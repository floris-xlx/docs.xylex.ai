import os
import subprocess
import shutil
from dotenv import load_dotenv


async def clone_and_checkout():
    load_dotenv()  # Load environment variables from .env file
    github_token = os.getenv("XLX_DOCS_GITHUB_TOKEN")
    if not github_token:
        raise EnvironmentError("GitHub token not found in environment variables")

    repo_url = f"https://floris-xlx:{github_token}@github.com/floris-xlx/xylex.git"
    cache_dir = "cache"
    repo_dir = os.path.join(cache_dir, "xylex")
    api_src_dir = os.path.join(repo_dir, "services/xylex_api_frontend/src/api")
    main_rs_file_path = os.path.join(
        repo_dir, "services/xylex_api_frontend/src/main.rs"
    )
    dest_dir = os.path.join(cache_dir, "api")

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    commands = [
        f"git clone --filter=blob:none --no-checkout --depth 1 {repo_url} {repo_dir}",
        f"cd {repo_dir}",
        "git sparse-checkout set --cone",
        "git checkout main",
        "git sparse-checkout set services/xylex_api_frontend/src",
    ]

    full_command = " && ".join(commands)
    subprocess.run(full_command, shell=True, check=True)

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(api_src_dir, dest_dir)
    shutil.copy(main_rs_file_path, os.path.join(cache_dir, "main.rs"))
    print(f"Cloned and checked out the repository to '{dest_dir}'.")

    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
        print(f"Deleted the directory '{repo_dir}'.")
    else:
        print(f"The directory '{repo_dir}' does not exist.")
