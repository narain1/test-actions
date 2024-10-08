import subprocess
import glob, os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Process GitHub PR data")

# Add arguments for tag name, PR title, and PR description
parser.add_argument('--tag_name', type=str, required=True, help="Tag name for the PR")
parser.add_argument('--pr_title', type=str, required=True, help="Title of the pull request")
parser.add_argument('--pr_description', type=str, required=True, help="Description of the pull request")

# Parse the arguments
args = parser.parse_args()
tag_name = args.tag_name
pr_title = args.pr_title
pr_description = args.pr_description

print("Tag name", tag_name)
print("pr title", pr_title)
print("pr description", pr_description)

# Convert single newlines to newline with two spaces for Markdown formatting
escaped_pr_description = pr_description.replace('\n', '  \n')
escaped_pr_description = escaped_pr_description.replace('### ', '\n### ').replace('- ', '\n- ')

release_notes = f"**Title:** {pr_title}\n**Description:** {escaped_pr_description}"

# Create GitHub release using gh CLI
try:
    directory = 'containers/lambda'
    zip_files = glob.glob(os.path.join(directory, '*.zip'))
    result = subprocess.run(
        ['gh', 'release', 'create', tag_name, '--title', tag_name, '--notes', release_notes],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"Release created successfully:\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error while creating release:\n{e.stderr}")
