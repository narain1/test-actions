import argparse
import subprocess
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Create a GitHub release with a tag, title, and description.")
parser.add_argument('--tag_name', required=True, help='The tag name for the release')
parser.add_argument('--pr_title', required=True, help='The pull request title')
parser.add_argument('--pr_description', required=True, help='The pull request description')

# Parse the arguments
args = parser.parse_args()

tag_name = args.tag_name
pr_title = args.pr_title
pr_description = args.pr_description

# Convert single newlines to newline with two spaces for Markdown formatting
escaped_pr_description = pr_description.replace('\n', '  \n')
escaped_pr_description = escaped_pr_description.replace('### ', '\n### ').replace('- ', '\n- ')

release_notes = f"**Title:** {pr_title}\n**Description:** {escaped_pr_description}"

# Create GitHub release using gh CLI
try:
    print(os.listdir('containers/lambda'))
    result = subprocess.run(
        ['gh', 'release', 'create', tag_name, 'containers/lambda/*.zip', '--title', tag_name, '--notes', release_notes],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"Release created successfully:\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error while creating release:\n{e.stderr}")
