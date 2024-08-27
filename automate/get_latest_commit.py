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
repo_watch_for_change_path = config['github_target']['repo_watch_for_change_path']
repo_owner, repo_name = repo_url.split('/')[-2], repo_url.split('/')[-1]



async def fetch_latest_commit():
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?page=1&per_page=1&path={repo_watch_for_change_path}"
    github_token = os.getenv("XLX_DOCS_GITHUB_TOKEN")
    headers = {'Authorization': f'token {github_token}'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_text = await response.text()
            print(response_text)


# To run the async function
# asyncio.run(fetch_latest_commit())
