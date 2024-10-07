import os
import subprocess

# Fetch PR details from the GitHub event
tag_name = f"r{os.getenv('GITHUB_EVENT_NUMBER')}"
pr_title = os.getenv('GITHUB_EVENT_PULL_REQUEST_TITLE')
pr_description = os.getenv('GITHUB_EVENT_PULL_REQUEST_BODY')

# Convert single newlines to newline with two spaces for Markdown formatting
escaped_pr_description = pr_description.replace('\n', '  \n')
escaped_pr_description = escaped_pr_description.replace('### ', '\n### ').replace('- ', '\n- ')

release_notes = f"**Title:** {pr_title}\n**Description:** {escaped_pr_description}"

# Create GitHub release using gh CLI
try:
    result = subprocess.run(
        ['gh', 'release', 'create', tag_name, 'containers/lambda/*.zip', '--title', tag_name, '--notes', release_notes],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print(f"Release created successfully:\n{result.stdout}")
except subprocess.CalledProcessError as e:
    print(f"Error while creating release:\n{e.stderr}")v