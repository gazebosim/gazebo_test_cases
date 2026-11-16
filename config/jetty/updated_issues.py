import os
import requests
from datetime import datetime, timedelta, timezone

# --- Configuration ---
# For security, load these from environment variables.
# How to set them:
# Linux/macOS: export GITHUB_TOKEN="your_token"
# Windows: set GITHUB_TOKEN="your_token"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = os.getenv("REPO_OWNER") # e.g., "microsoft"
REPO_NAME = os.getenv("REPO_NAME")   # e.g., "vscode"

def find_recently_renamed_issues():
    """
    Finds issues in a GitHub repository whose titles have been
    renamed within the last hour.
    """
    if not all([GITHUB_TOKEN, REPO_OWNER, REPO_NAME]):
        print("Error: Make sure GITHUB_TOKEN, REPO_OWNER, and REPO_NAME environment variables are set.")
        return

    # 1. Calculate the timestamp for one hour ago in UTC (ISO 8601 format)
    # GitHub API uses the ISO 8601 format for timestamps.
    time_one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=3)
    since_timestamp = time_one_hour_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    print(f"Searching for issues in '{REPO_OWNER}/{REPO_NAME}' updated since {since_timestamp}...")

    # 2. Set up headers for API authentication
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # 3. API URL to get all issues updated in the last hour
    issues_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    params = {
        "since": since_timestamp,
        "state": "all" # Check both open and closed issues
    }

    try:
        # 4. Fetch the list of issues updated recently
        response = requests.get(issues_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        issues = response.json()

        if not issues:
            print("No issues have been updated in the last hour.")
            return

        print(f"Found {len(issues)} issues updated in the last hour. Checking their timelines for title changes...")
        renamed_issues_found = 0

        # 5. Iterate through each updated issue to check its event timeline
        for issue in issues:
            issue_number = issue['number']
            timeline_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/timeline"
            
            # Use pagination for timelines that might be very long
            page = 1
            while True:
                timeline_params = {"per_page": 100, "page": page}
                timeline_response = requests.get(timeline_url, headers=headers, params=timeline_params)
                timeline_response.raise_for_status()
                timeline_events = timeline_response.json()

                if not timeline_events:
                    break # Exit loop if no more events on subsequent pages

                print(f"URL: {issue['html_url']}, {issue['title']}")
                
                # Check if we need to continue to the next page of timeline events
                if 'next' not in timeline_response.links:
                    break
                page += 1
            
        if renamed_issues_found == 0:
            print("\nNo issues had their titles changed in the last hour.")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        if response.status_code == 401:
            print("Authentication failed. Please check your GITHUB_TOKEN.")
        elif response.status_code == 404:
            print(f"Repository '{REPO_OWNER}/{REPO_NAME}' not found. Please check REPO_OWNER and REPO_NAME.")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    find_recently_renamed_issues()
