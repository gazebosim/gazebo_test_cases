from github import Github
import os
import jinja2
import argparse

valid_labels = ["not-started", "completion-1", "completion-2", "completion-3"]
score_multiplier_labels = { "os: Windows":  1.2, "os: MacOS": 1.2}
score_difficulty_labels = { "easy":  6, "hard": 18}
needs_review_labels = ["failed", "fixed"]
needs_review_emoji = [":x:", ":negative_squared_cross_mark:"]
completion_keywords = ["[status: passed]", "[status: failed]"]
score_board = {}

leaderboard_template = r"""
# **LEADER BOARD**

| **Place** | **User** | **Points** | **Contributions** |
| :-------: | :-------: | :------: | :-------: |
{% for user in users -%}
| {{ loop.index }} | <img src="{{ users[user].avatar_url }}" alt="{{ user }}" width="128" height="128"> <br> [{{ user }}](https://github.com/{{ user }}) <br> **Unique Completed: {{ users[user].number_unique_completed }}** <br> $${{ '{' }}\color{{ '{' }}green{{ '}' }}First \space Completed: \space {{ users[user].number_first_completed }}{{ '}' }}$$ <br> $${{ '{' }}\color{{ '{' }}yellow{{ '}' }}Second \space Completed: \space {{ users[user].number_second_completed }}{{ '}' }}$$ <br> $${{ '{' }}\color{{ '{' }}red{{ '}' }}Third \space Completed: \space {{ users[user].number_third_completed }}{{ '}' }}$$ <br> Total Completed: {{ users[user].number_completed }} | {{ users[user].score|round(2) }}  | {% for issue in users[user].issues %}[#{{ issue }} +{{ users[user]['issues'][issue].points|round(2) }}]({{ users[user]['issues'][issue].comment_url }}) $${{ '{' }}\color{{ '{' }}{%- if  users[user]['issues'][issue].completer_number == 1 -%}green{%- elif  users[user]['issues'][issue].completer_number == 2 -%}yellow{%- else -%}red{%- endif -%}{{ '}' }}({{ users[user]['issues'][issue].completer_number }}/{{ users[user]['issues'][issue].number_completions}}){{ '}' }}$$ {{ users[user]['issues'][issue].emoji }} {% if loop.index % 3 == 0 %}<br>{% endif %} {% endfor %} |
{% endfor %}
"""

template = jinja2.Template(leaderboard_template)

g = Github(os.getenv("GITHUB_TOKEN"))

def get_repo_object(owner, repo_name):
    try:
        repo = g.get_user(owner).get_repo(repo_name)
        return repo
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_issue_object(repo, issue_number):
    try:
        issue = repo.get_issue(number=issue_number)
        return issue
    except Exception as e:
        print(f"Error: {e}")
        return []

def get_issue_details(issue, issue_number):
    try:
        comments_data = []
        label_data = []
        assignee_data = []
        ignore_completer = ["caguero", "mjcarroll", "iche033", "ahcorde", "jennuine", "bperseghetti", "scpeters", "jrivero", "traversaro", "azeey"]
        unique_completer = []
        for assignee in issue.assignees:
            assignee_data.append(assignee.login)
        for label in issue.get_labels():
            if (label.name in valid_labels or
                label.name in score_multiplier_labels or
                label.name in score_difficulty_labels or
                label.name in needs_review_labels):
                label_data.append(label.name)
        for comment in issue.get_comments():
            sanitized_comment = comment.body.replace(f"> {completion_keywords[0]}","").replace(f"> {completion_keywords[1]}","")
            if (completion_keywords[0] in sanitized_comment or
                completion_keywords[1] in sanitized_comment):
                if (comment.user.login not in unique_completer and
                    comment.user.login not in ignore_completer):
                    print(f"Issue: #{issue_number} - Adding completer: {comment.user.login}")
                    unique_completer.append(comment.user.login)
                    comments_data.append({
                        'user': comment.user.login,
                        'body': comment.body,
                        'url': comment.html_url
                    })
                else:
                    print(f"Issue: #{issue_number} - Ignoring completer: {comment.user.login}")
        return comments_data, label_data, assignee_data, issue.title
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def evaluate_completions (comment_completion, issue_labels, issue_assignees, issue_title, issue_number, issue):
        score_multiplier = 1
        score_base_value = 12
        unique_completion = 1
        for score_label in issue_labels:
            if score_label in score_multiplier_labels:
                score_multiplier = score_multiplier_labels[score_label]
                print(f"Issue: #{issue_number} - label: { score_label } modifying multiplier: {score_multiplier} ")
            if score_label in score_difficulty_labels:
                score_base_value = score_difficulty_labels[score_label]
                print(f"Issue: #{issue_number} - label: { score_label } modifying difficulty value: {score_base_value} ")
        score_value = score_multiplier * score_base_value
        number_completions = len(comment_completion)
        if number_completions > 1:
            unique_completion = 0
        if number_completions > 3:
            print(f"Issue: #{issue_number} -  exceeds limit of 3 completers with value of {number_completions}.")
            comment_completion=comment_completion[:3]
            number_completions = 3
        if number_completions <= 3:
            if valid_labels[number_completions] not in issue_labels:
                for label in issue_labels:
                    if label in valid_labels:
                        print(f"Issue: #{issue_number} - Removing label: {label}")
                        issue.remove_from_labels(label)
                print(f"Issue: #{issue_number} - Adding label: {valid_labels[number_completions]}")
                issue.add_to_labels(valid_labels[number_completions])
            completer_number=0
            for comment in comment_completion:
                completer_number+=1
                completion_emoji="  "
                if completion_keywords[1] in comment["body"]:
                    if needs_review_labels[0] not in issue_labels:
                        issue.add_to_labels(needs_review_labels[0])
                        completion_emoji=needs_review_emoji[0]
                        print(f"Issue: #{issue_number} - completed as failed, label added")
                    elif needs_review_labels[1] in issue_labels:
                        completion_emoji=needs_review_emoji[1]
                        print(f"Issue: #{issue_number} - completed as failed but fix confirmed")
                    else:
                        completion_emoji=needs_review_emoji[0]
                        print(f"Issue: #{issue_number} - completed as failed, no fix yet")
                if comment["user"] not in issue_assignees:
                    print(f"Issue: #{issue_number} - Adding assignee: {comment["user"]}")
                    issue.add_to_assignees(comment["user"])
                if comment['user'] not in score_board:
                    score_board[comment['user']] = {
                        "issues": {},
                        "score": score_value/number_completions,
                        "avatar_url": g.get_user(comment['user']).avatar_url,
                        "number_completed": 1,
                        "number_unique_completed": unique_completion,
                        "number_first_completed": 1 if completer_number == 1 else 0 ,
                        "number_second_completed": 1 if completer_number == 2 else 0 ,
                        "number_third_completed": 1 if completer_number == 3 else 0
                        }
                    score_board[comment['user']]['issues'][issue_number] = {
                        "comment_url": comment["url"],
                        "points": score_value/number_completions,
                        "emoji": completion_emoji,
                        "completer_number": completer_number,
                        "number_completions": number_completions
                        }
                else:
                    score_board[comment['user']]['issues'][issue_number]={
                        "comment_url": comment["url"],
                        "points": score_value/number_completions,
                        "emoji": completion_emoji,
                        "completer_number": completer_number,
                        "number_completions": number_completions
                    }
                    score_board[comment['user']]['score']+=score_value/number_completions
                    score_board[comment['user']]['number_completed']+=1
                    score_board[comment['user']]['number_first_completed']+=1 if completer_number == 1 else 0
                    score_board[comment['user']]['number_second_completed']+=1 if completer_number == 2 else 0
                    score_board[comment['user']]['number_third_completed']+=1 if completer_number == 3 else 0
                    score_board[comment['user']]['number_unique_completed']+=unique_completion

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--owner", type=str, default="gazebosim", help="Owner of the repository")
    parser.add_argument("-r", "--repository", type=str, default="gazebo_test_cases", help="Repository to score issues over")
    parser.add_argument("-l", "--label", type=str, default="ionic", help="Label to get relevant issues from")
    args = parser.parse_args()

    repo_owner = args.owner
    repository_name = args.repository
    target_label = args.label
    i=0
    target_repo = get_repo_object(repo_owner, repository_name)

    repo_issues_object = list(target_repo.get_issues(state="all", labels=[target_label]))
    num_issues = len(repo_issues_object)
    for issue_object in repo_issues_object:
        
        target_issue_number = issue_object.number
        i+=1
        print(f"Processing #{target_issue_number} - ({i}/{num_issues})")
        
    
        comments, labels, assignees, title = get_issue_details(issue_object, target_issue_number)
    
        if labels and comments:
            evaluate_completions(comments, labels, assignees, title, target_issue_number, issue_object)
        
    sorted_score_board = dict(sorted(score_board.items(), key=lambda item: item[1]["score"], reverse=True))

    leader_board_md = template.render(users=sorted_score_board)
    try:
        file_name = f"{target_label.upper()}_LEADER_BOARD.md"
        branch_name="leaderboard"
        contents = target_repo.get_contents(file_name, ref=branch_name)
        target_repo.update_file(contents.path, f"Update {file_name}", leader_board_md, contents.sha, branch=branch_name)
        print(f"{file_name} UPDATED")
    except Exception:
        target_repo.create_file(file_name, f"Update {file_name}", leader_board_md, branch=branch_name)
        print(f"{file_name} CREATED")
    try:
        file_name_readme = "README.md"
        branch_name="leaderboard"
        contents = target_repo.get_contents("README.md", ref=branch_name)
        target_repo.update_file(contents.path, "Update README.md", leader_board_md, contents.sha, branch=branch_name)
        print("README.md UPDATED")
    except Exception:
        target_repo.create_file("README.md", f"Update README.md", leader_board_md, branch=branch_name)
        print("README.md CREATED")
