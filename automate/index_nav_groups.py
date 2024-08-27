import os
import json

MINT_CONFIG = 'mint.json'
CACHE_API_PATH = 'cache/api'


def check_directory_exists(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The directory '{path}' does not exist.")


async def list_folders_in_cache_api():
    check_directory_exists(CACHE_API_PATH)
    folders = [
        name for name in os.listdir(CACHE_API_PATH)
        if os.path.isdir(os.path.join(CACHE_API_PATH, name))
    ]
    print(f"Navigation indexes in '{CACHE_API_PATH}': {folders}")
    return folders


async def get_navigation_groups():
    with open(MINT_CONFIG, 'r') as file:
        data = json.load(file)
    navigation_groups = [
        group['group'] for group in data.get('navigation', [])
    ]
    print(f"Navigation groups in {MINT_CONFIG}: {navigation_groups}")
    return navigation_groups


async def get_top_level_folders_excluding_mod_rs():
    check_directory_exists(CACHE_API_PATH)
    top_level_folders = {
        name: [
            file_name
            for file_name in os.listdir(os.path.join(CACHE_API_PATH, name))
            if os.path.isfile(os.path.join(CACHE_API_PATH, name, file_name))
            and file_name != 'mod.rs'
        ]
        for name in os.listdir(CACHE_API_PATH)
        if os.path.isdir(os.path.join(CACHE_API_PATH, name))
    }
    print(
        f"Top-level folders and files (excluding 'mod.rs') in '{CACHE_API_PATH}': {top_level_folders}"
    )
    return top_level_folders


async def update_navigation_groups():
    top_level_folders = await get_top_level_folders_excluding_mod_rs()
    print(f"top_level_folders: {top_level_folders}")

    with open(MINT_CONFIG, 'r') as file:
        data = json.load(file)

    existing_groups = {group['group'] for group in data.get('navigation', [])}
    new_groups = [
        folder.capitalize() for folder in top_level_folders.keys()
        if f"{folder.capitalize()} API" not in existing_groups
    ]

    unique_folders = sorted(set(new_groups))
    unique_folders_and_files = {
        folder: sorted(set(files))
        for folder, files in top_level_folders.items()
    }

    for new_group in unique_folders:
        group_key = f"{new_group} API"
        pages_path = [
            f"{new_group.lower()}/{file}"
            for file in unique_folders_and_files[new_group.lower()]
        ]
        data['navigation'].append({"group": group_key, "pages": pages_path})

    with open(MINT_CONFIG, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated navigation groups in {MINT_CONFIG} with: {unique_folders}")
    return unique_folders
