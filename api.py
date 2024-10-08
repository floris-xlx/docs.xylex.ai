from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


class APIKeyHeader(BaseModel):
    api_key: str


import json
import asyncio
from automate.clear_cache import clear_cache
from automate.get_repo import clone_and_checkout
from automate.index_nav_groups import list_folders_in_cache_api, get_navigation_groups, update_navigation_groups
from automate.get_latest_commit import fetch_latest_commit
from automate.sync_nav_tags import sync_nav_tags
from automate.endpoint_router import find_and_extract_endpoints
from automate.content_framer import update_mdx_files_with_parameters
from automate.deduplicator import remove_duplicates_from_mdx
from automate.github_jwt_key import generate_jwt, generate_installation_token
from automate.add_commit_status import post_commit_comment, post_commit_status_with_jwt


async def build_docs_client():
    await clear_cache()
    await clone_and_checkout()
    await list_folders_in_cache_api()
    await get_navigation_groups()
    await update_navigation_groups()
    await fetch_latest_commit()
    sync_nav_tags()

    endpoints = find_and_extract_endpoints()
    print(json.dumps(endpoints, indent=4))

    import concurrent.futures

    def update_mdx_files_with_parameters_thread(endpoint):
        print(f"Starting thread for endpoint: {endpoint['endpoint']}")
        asyncio.run(update_mdx_files_with_parameters([endpoint]))
        print(f"Finished thread for endpoint: {endpoint['endpoint']}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        print(
            "Starting ThreadPoolExecutor for updating MDX files with parameters."
        )
        executor.map(update_mdx_files_with_parameters_thread, endpoints)
        print("Completed all threads for updating MDX files with parameters.")

    for endpoint in endpoints:
        mdx_filepath = endpoint.get("mdx_filepath")
        if mdx_filepath:
            await remove_duplicates_from_mdx(mdx_filepath)

    sync_nav_tags()

    # print in bold green success message and then git add . && git commit -m "Generated API docs" && git push --force
    print("\033[1m\033[92mSuccessfully generated API docs!\033[0m")
    print("\033[1m\033[92mPushing changes to the repository...\033[0m")

    import subprocess

    # Execute shell command to add changes, commit, and push with authentication
    from dotenv import load_dotenv
    import os

    load_dotenv()  # Load environment variables from .env file

    # Set up the remote URL with authentication

    # Add changes, commit, and push with JWT authentication
    jwt_key = generate_jwt()
    print(jwt_key)
    install_token = generate_installation_token(jwt_key)
    print(install_token)

    import os
    import glob

    # Find all files in the root directory that contain 'nohup' in their name
    nohup_files = glob.glob('nohup*')

    # Delete each file found
    for file in nohup_files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")

    user_access_token = os.getenv("XLX_DOCS_GITHUB_TOKEN")
    subprocess.run("git config --global user.name 'floris-xlx'",
                   shell=True,
                   check=True)
    subprocess.run("git config --global user.email 'floris@xylex.ai'",
                   shell=True,
                   check=True)
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run('git commit -m "Generated API docs"',
                   shell=True,
                   check=True)
    subprocess.run(
        f"git remote set-url origin https://x-access-token:{user_access_token}@github.com/floris-xlx/docs.xylex.ai.git",
        shell=True,
        check=True)
    subprocess.run("git push --force", shell=True, check=True)


import requests
import os


def get_api_key(api_key_header: APIKeyHeader):
    load_dotenv()

    api_key = os.getenv("XLX_DOCS_XYLEX_API_KEY")
    if api_key_header.api_key != api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header.api_key


async def handle_commit_messaging():
    # Fetch the latest commit details
    commit_message, sha, committer_login, sha_short = await fetch_latest_commit(
    )

    # Post a commit comment using the short SHA
    comment_body = f"Successfully built the documentation for commit {sha_short} by {committer_login}, View the documentation at [https://nightly.docs.xylex.ai/](https://nightly.docs.xylex.ai/)"
    post_commit_comment(sha_short, comment_body)

    # Post a commit status using the full SHA
    post_commit_status_with_jwt(sha)


@app.get("/build-docs")
async def build_docs(api_key: str):
    api_key = get_api_key(APIKeyHeader(api_key=api_key))
    await build_docs_client()
    await handle_commit_messaging()
    return {"message": "Docs built successfully!"}


# Call the function to handle messaging

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3398)
