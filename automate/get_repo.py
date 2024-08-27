
import os
import subprocess
from dotenv import load_dotenv

def clone_and_checkout():
    load_dotenv()  # Load environment variables from .env file
    github_token = os.getenv('XLX_DOCS_GITHUB_TOKEN')
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")

    repo_url = f"https://floris-xlx:{github_token}@github.com/floris-xlx/xylex.git"
    commands = [
        "cd cache",
        f"git clone --filter=blob:none --no-checkout --depth 1 {repo_url}",
        "cd xylex",
        "git sparse-checkout set --cone",
        "git checkout main",
        "git sparse-checkout set services/xylex_api_frontend"
    ]

    full_command = " && ".join(commands)
    subprocess.run(full_command, shell=True, check=True)

if __name__ == '__main__':
    clone_and_checkout()
