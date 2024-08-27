import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import yaml

load_dotenv()  # Load environment variables from .env file

# Load the YAML configuration file
with open('auto-generate-config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extract repo owner and repo name from the YAML configuration
repo_url = config['github_target']['repo_url']
path = config['github_target']['repo_watch_for_change_path']
repo_owner, repo_name = repo_url.split('/')[-2], repo_url.split('/')[-1]


async def fetch_latest_commit():
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?page=1&per_page=1&path={path}"
    github_token = os.getenv("XLX_DOCS_GITHUB_TOKEN")
    headers = {'Authorization': f'token {github_token}'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_json = await response.json()

            # Extract the required information
            commit_message = response_json[0]['commit']['message']
            sha = response_json[0]['sha']
            committer_login = response_json[0]['committer']['login']
            print(f"Commit Message: {commit_message}\nSHA: {sha}\nCommitter: {committer_login}")
            return commit_message, sha, committer_login

