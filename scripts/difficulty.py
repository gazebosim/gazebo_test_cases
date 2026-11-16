import re
import math
import os
import argparse
from ruamel.yaml import YAML

# --- Configuration ---
WPM = 225  # Average words per minute for reading prose
SECONDS_PER_IMAGE = 10  # Estimated time to view and understand an image
CACHE_DIR = ".cache"  # The directory where cloned repositories are stored


def get_local_path_from_url(url: str) -> str | None:
    """
    Converts a GitHub file URL to its corresponding local path in the .cache directory.

    Args:
        url: The full URL to the markdown file on GitHub.

    Returns:
        The local file path or None if the URL pattern doesn't match.
    """
    # This regex captures the owner, repository name, and the file path within the repo.
    # It handles both '/tree/' and '/blob/' paths common in GitHub URLs.
    match = re.search(r"github\.com/([^/]+)/([^/]+)/(?:tree|blob)/[^/]+/(.*)", url)
    if not match:
        return None

    owner_name = match.group(1)
    repo_name = match.group(2)
    file_path_in_repo = match.group(3)

    return os.path.join(CACHE_DIR, owner_name, repo_name, file_path_in_repo)


def calculate_difficulty(file_path: str) -> str | None:
    """
    Estimates reading time for a markdown file and returns a difficulty level.

    Args:
        file_path: The local path to the markdown file.

    Returns:
        A string ('easy', 'medium', 'hard') or None if the file can't be processed.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"⚠️  Warning: File not found at '{file_path}'. Skipping.")
        return None
    except Exception as e:
        print(f"❌ Error reading file '{file_path}': {e}")
        return None

    # 1. Count images and calculate time spent on them
    image_count = len(re.findall(r"!\[.*?\]\(.*?\)", content))
    image_time_seconds = image_count * SECONDS_PER_IMAGE

    # 2. Remove non-prose elements before counting words
    prose_content = content
    # prose_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL) # Code blocks
    # prose_content = re.sub(r'`[^`]*`', '', prose_content)              # Inline code
    prose_content = re.sub(r"!\[.*?\]\(.*?\)", "", prose_content)  # Images
    prose_content = re.sub(r"<.*?>", "", prose_content)  # HTML tags
    prose_content = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", prose_content)  # Links
    prose_content = re.sub(r"[#*_-]", "", prose_content)  # Markdown symbols

    # 3. Count words and calculate total reading time in minutes
    word_count = len(prose_content.split())
    prose_time_minutes = word_count / WPM
    total_time_minutes = prose_time_minutes + (image_time_seconds / 60)
    display_time = math.ceil(total_time_minutes)
    # print(file_path, display_time)

    # 4. Assign a difficulty level based on the time
    if display_time < 3:
        return "easy"
    elif 3 <= display_time <= 8:
        return "medium"
    else:
        return "hard"


def process_yaml(input_path: str, output_path: str):
    """
    Reads a YAML file, adds difficulty labels, and writes to a new file.
    """
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at '{input_path}'")
        return

    if "requirements" not in data or not isinstance(data["requirements"], list):
        print("❌ Error: YAML must contain a list under the 'requirements' key.")
        return

    print(f"Processing '{input_path}'...")
    for req in data.get("requirements", []):
        source_link = next(
            (link for link in req.get("links", []) if link.get("name") == "Source"),
            None,
        )

        if not source_link or "url" not in source_link:
            print(f"-> Skipping '{req.get('name', 'N/A')}': No 'Source' link found.")
            continue

        url = source_link["url"]
        local_path = get_local_path_from_url(url)

        if not local_path:
            print(
                f"-> Skipping '{req.get('name', 'N/A')}': Could not parse GitHub URL '{url}'."
            )
            continue

        if not local_path.endswith(".md"):
            print(
                f"-> Skipping '{req.get('name', 'N/A')}': Not a markdown file '{local_path}'."
            )
            continue

        difficulty = calculate_difficulty(local_path)

        # Only add 'easy' or 'hard' labels
        if difficulty in ["easy", "hard"]:
            if "labels" not in req:
                req["labels"] = []

            if difficulty not in req["labels"]:
                req["labels"].append(difficulty)
                print(f"✅ Added label '{difficulty}' to '{req.get('name', 'N/A')}'")

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
        print(f"\n✨ Successfully processed YAML. Output saved to '{output_path}'")
    except Exception as e:
        print(f"❌ Error writing to output file '{output_path}': {e}")


def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Assign difficulty labels to markdown files listed in a YAML file.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the input YAML file."
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Path for the output YAML file."
    )
    args = parser.parse_args()
    process_yaml(args.input, args.output)


if __name__ == "__main__":
    main()
