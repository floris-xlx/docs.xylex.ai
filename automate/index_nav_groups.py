import os
import json

MINT_CONFIG = 'mint.json'

async def list_folders_in_cache_api():
    cache_api_path = 'cache/api'
    if not os.path.exists(cache_api_path):
        raise FileNotFoundError(
            f"The directory '{cache_api_path}' does not exist.")

    folders = [
        name for name in os.listdir(cache_api_path)
        if os.path.isdir(os.path.join(cache_api_path, name))
    ]
    print(f"Navigation indexes in 'cache/api': {folders}")
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
    cache_api_path = 'cache/api'
    if not os.path.exists(cache_api_path):
        raise FileNotFoundError(
            f"The directory '{cache_api_path}' does not exist.")

    top_level_folders = {}
    for name in os.listdir(cache_api_path):
        folder_path = os.path.join(cache_api_path, name)
        if os.path.isdir(folder_path):
            # Only consider top-level folders
            files = [
                file_name for file_name in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file_name)) and file_name != 'mod.rs'
            ]
            top_level_folders[name] = files

    print(f"Top-level folders and files (excluding 'mod.rs') in 'cache/api': {top_level_folders}")
    return top_level_folders


async def update_navigation_groups():
    # Get the current top-level folders and files in 'cache/api', excluding 'mod.rs'
    top_level_folders = await get_top_level_folders_excluding_mod_rs()
    print(f"top_level_folders: {top_level_folders}")

    # Open and load the mint.json file
    with open(MINT_CONFIG, 'r') as file:
        data = json.load(file)

    # Extract existing navigation groups
    existing_groups = {group['group'] for group in data.get('navigation', [])}

    # Determine which top-level folders are not in the existing groups
    new_groups = []
    for folder in top_level_folders.keys():
        group_key = folder.capitalize() + " API"
        if group_key not in existing_groups:
            new_groups.append(folder.capitalize())

    # Sort the folders and files for uniqueness
    unique_folders = sorted(set(new_groups))
    unique_folders_and_files = {
        folder: sorted(set(files)) for folder, files in top_level_folders.items()
    }

    # Add new groups to the navigation section
    for new_group in unique_folders:
        group_key = new_group + " API"
        pages_path = [
            f"{new_group.lower()}/{file}"
            for file in unique_folders_and_files[new_group.lower()]
        ]
        data['navigation'].append({"group": group_key, "pages": pages_path})

    # Write the updated data back to MINT_CONFIG
    with open(MINT_CONFIG, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated navigation groups in {MINT_CONFIG} with: {unique_folders}")
    return unique_folders
