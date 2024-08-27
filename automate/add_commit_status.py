import os
import json
import requests
from dotenv import load_dotenv
import yaml

load_dotenv()

# Load configuration from YAML file
with open('auto-generate-config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extract necessary values from the YAML configuration
repo_owner = config['github_target']['repo_url'].split('/')[-2]
repo_name = config['github_target']['repo_url'].split('/')[-1]

def post_commit_status(commit_sha):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/statuses/{commit_sha}"
    payload = json.dumps({
        "state": "success",
        "target_url": "https://nightly.docs.xylex.ai/",
        "description": "The build succeeded!",
        "context": "xylex-buildpack/docs.xylex.ai / build"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.getenv('XLX_DOCS_GITHUB_TOKEN')}"
    }

    response = requests.post(url, headers=headers, data=payload)
    print(response.text)

# Example usage
post_commit_status('66051cc18683301ec135ba125f3377634d086983')


