from github import Github
import os
import jinja2

valid_labels = ["not-started", "completion-1", "completion-2", "completion-3"]
score_board = {}

leaderboard_template = """
# **LEADER BOARD**

| **User** | **Points** | **Contributions** |
| :-------: | :------: | :-------: |
{% for user in users -%}
| ![{{ user }}]( {{ users[user].avatar_url }} "{{ user }}")  | {{ users[user].score }}  | {% for issue in users[user].issues %}[#{{ issue }} +{{ users[user]['issues'][issue].points }}]({{ users[user]['issues'][issue].comment_url }}) {% endfor %} |
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


def get_issue_details(issue):
    try:
        comments_data = []
        label_data = []
        assignee_data = []
        unique_completer = []
        for assignee in issue.assignees:
            assignee_data.append(assignee.login)
        
        for label in issue.get_labels():
            if label.name in valid_labels:
                label_data.append(label.name)

        for comment in issue.get_comments():
            sanitized_comment = comment.body.replace("> [status: failed]","").replace("> [status: passed]","")
            if "[status: passed]" in sanitized_comment or "[status: failed]" in sanitized_comment and comment.user.login not in unique_completer:
                unique_completer.append(comment.user.login)
                comments_data.append({
                    'user': comment.user.login,
                    'body': comment.body,
                    'url': comment.html_url
            })

        return comments_data, label_data, assignee_data, issue.title
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def evaluate_completions (comment_completion, issue_labels, issue_assignees, issue_title, issue_number, issue):
        score_base_value = 6
        number_completions = len(comment_completion)
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
                
            for comment in comment_completion:
                if comment["user"] not in issue_assignees:
                    print(f"Issue: #{issue_number} - Adding assignee: {comment["user"]}")
                    issue.add_to_assignees(comment["user"])
                        
                if comment['user'] not in score_board:

                    score_board[comment['user']] = {
                        "issues": {},
                        "score": score_base_value/number_completions,
                        "avatar_url": g.get_user(comment['user']).avatar_url
                        }

                    score_board[comment['user']]['issues'][issue_number] = {
                        "comment_url": comment["url"],
                        "points": score_base_value/number_completions
                        }
                else: 
                    score_board[comment['user']]['issues'][issue_number]={
                        "comment_url": comment["url"],
                        "points": score_base_value/number_completions
                    }
                    score_board[comment['user']]['score']+=score_base_value/number_completions    

        
if __name__ == "__main__":
    repo_owner = "gazebosim" 
    repository_name = "gazebo_test_cases"
    start_issue = 1500
    end_issue = 1560
    targets = range(start_issue, end_issue+1)
    num_issues=end_issue-start_issue
    i=0
    target_repo = get_repo_object(repo_owner, repository_name)
    
    for target_issue_number in targets:
        i+=1
        print(f"Processing #{target_issue_number} - ({i}/{num_issues})")
        issue_object = get_issue_object(target_repo, target_issue_number)
    
        comments, labels, assignees, title = get_issue_details(issue_object)
    
        if labels and comments:
            evaluate_completions(comments, labels, assignees, title, target_issue_number, issue_object)
        
    sorted_score_board = dict(sorted(score_board.items(), key=lambda item: item[1]["score"], reverse=True))

    leader_board_md = template.render(users=sorted_score_board)
    try:
        file_name = "LEADER_BOARD.md"
        branch_name="test_points"
        contents = target_repo.get_contents(file_name, ref=branch_name)
        target_repo.update_file(contents.path, "Update LEADER_BOARD.md", leader_board_md, contents.sha, branch=branch_name)
        print(f"{file_name} UPDATED")
    except Exception:
        target_repo.create_file(file_name, "Update LEADER_BOARD.md", leader_board_md, branch=branch_name)
        print(f"{file_name} CREATED")