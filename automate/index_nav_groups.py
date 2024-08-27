import os
import json

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
    with open('mint.json', 'r') as file:
        data = json.load(file)

    navigation_groups = [
        group['group'] for group in data.get('navigation', [])
    ]

    print(f"Navigation groups in 'mint.json': {navigation_groups}")
    return navigation_groups


async def update_navigation_groups():
    # Get the current folders in 'cache/api'
    folders = await list_folders_in_cache_api()

    # Open and load the mint.json file
    with open('mint.json', 'r') as file:
        data = json.load(file)

    # Extract existing navigation groups
    existing_groups = {group['group'] for group in data.get('navigation', [])}

    # Determine which folders are not in the existing groups
    new_groups = [folder.capitalize() for folder in folders if folder.capitalize() not in existing_groups]

    # Add new groups to the navigation section
    for new_group in new_groups:
        data['navigation'].append({
            "group": new_group + " API",
            "pages": []  # Assuming new groups start with an empty pages list
        })

    # Write the updated data back to mint.json
    with open('mint.json', 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated navigation groups in 'mint.json' with: {new_groups}")
    return new_groups
