import subprocess
import glob, os
import shutil

tag_name = shutil.run("${{github.event.number }}", capture_output=True, text=True)
pr_title = shutil.run("${{github.event.pull_request.title }}", capture_output=True, text=True)
pr_description =shutil.run("${{github.event.pull_request.body}}", capture_output=True, text=True)

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
