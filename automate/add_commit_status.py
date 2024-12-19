import os
import json
import requests
from dotenv import load_dotenv
from automate.github_jwt_key import generate_jwt, generate_installation_token
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


def post_commit_status_with_jwt(commit_sha):
    # Generate JWT using the existing function
    jwt_key = generate_jwt()

    # Generate installation token using the JWT
    install_token = generate_installation_token(jwt_key)

    # Construct the URL for posting commit status
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/statuses/{commit_sha}"

    # Define the payload for the commit status
    payload = json.dumps({
        "state": "success",
        "target_url": "https://nightly.docs.xylex.ai/",
        "description": "The build succeeded!",
        "context": "xylex-buildpack/docs.xylex.ai / build"
    })

    # Set the headers including the installation token for authorization
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {install_token}"
    }

    # Make the POST request to set the commit status
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)



def post_commit_comment(commit_sha, comment_body):
    # Generate JWT using the existing function
    jwt_key = generate_jwt()

    # Generate installation token using the JWT
    install_token = generate_installation_token(jwt_key)

    # Construct the URL for posting commit comment
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}/comments"

    # Define the payload for the commit comment
    payload = json.dumps({
        "body": comment_body
    })

    # Set the headers including the installation token for authorization
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {install_token}"
    }

    # Make the POST request to add the commit comment
    response = requests.post(url, headers=headers, data=payload)
    print(response.text)
