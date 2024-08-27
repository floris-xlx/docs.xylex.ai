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


async def main():
    # await clear_cache()
    # await clone_and_checkout()
    # await list_folders_in_cache_api()
    # await get_navigation_groups()
    # await update_navigation_groups()
    # await fetch_latest_commit()
    # sync_nav_tags()

    # endpoints = find_and_extract_endpoints()
    # print(json.dumps(endpoints, indent=4))

    # import concurrent.futures

    # def update_mdx_files_with_parameters_thread(endpoint):
    #     print(f"Starting thread for endpoint: {endpoint['endpoint']}")
    #     asyncio.run(update_mdx_files_with_parameters([endpoint]))
    #     print(f"Finished thread for endpoint: {endpoint['endpoint']}")

    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     print("Starting ThreadPoolExecutor for updating MDX files with parameters.")
    #     executor.map(update_mdx_files_with_parameters_thread, endpoints)
    #     print("Completed all threads for updating MDX files with parameters.")

    # for endpoint in endpoints:
    #     mdx_filepath = endpoint.get("mdx_filepath")
    #     if mdx_filepath:
    #         await remove_duplicates_from_mdx(mdx_filepath)

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
    
    # Set the commit user to the app
    subprocess.run('git config user.name "xylex-buildpack"', shell=True, check=True)
    subprocess.run('git config user.email "app@xylex.ai"', shell=True, check=True)
    subprocess.run("git add .", shell=True, check=True)
    subprocess.run('git commit -m "Generated API docs"',
                   shell=True,
                   check=True)
    subprocess.run(
        f"git remote set-url origin https://x-access-token:{install_token}@github.com/floris-xlx/docs.xylex.ai.git",
        shell=True,
        check=True)
    subprocess.run("git push --force", shell=True, check=True)


if __name__ == '__main__':
    asyncio.run(main())


import requests
import os
