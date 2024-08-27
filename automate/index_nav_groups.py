import os
import json

MINT_CONFIG = 'mint.json'
CACHE_API_PATH = 'cache/api'

BANNED_PATHS = [
    'cache', 'automate', 'essentials', '.git', '.github', 'snippets', 'logos',
    'images'
]

from automate.parse_api_endpoint import extract_endpoints_from_rs_file


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
    top_level_folders = {}

    for name in os.listdir(CACHE_API_PATH):
        folder_path = os.path.join(CACHE_API_PATH, name)
        if os.path.isdir(folder_path):
            files = [
                file_name.replace('.rs', '')
                for file_name in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file_name))
                and file_name != 'mod.rs'
            ]

            # Look one folder deeper for 'endpoint.rs'
            for sub_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_name)
                if os.path.isdir(sub_folder_path):
                    if 'endpoint.rs' in os.listdir(sub_folder_path):
                        files.append(sub_name)

            top_level_folders[name] = files

    print(
        f"Top-level folders and files (excluding 'mod.rs') in '{CACHE_API_PATH}': {top_level_folders}"
    )
    return top_level_folders


def generate_pages_path(new_group, unique_folders_and_files):
    return [
        f"pages/{new_group.lower()}/{file}"
        for file in unique_folders_and_files[new_group.lower()]
    ]


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
        pages_path = generate_pages_path(new_group, unique_folders_and_files)
        if pages_path:  # Only add the group if pages_path is not empty
            data['navigation'].append({
                "group": group_key,
                "pages": pages_path
            })

    with open(MINT_CONFIG, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Updated navigation groups in {MINT_CONFIG} with: {unique_folders}")

    await create_group_folders_and_pages(top_level_folders)

    return unique_folders


async def create_group_folders_and_pages(top_level_folders):
    for group, pages in top_level_folders.items():
        if group.lower() not in BANNED_PATHS:
            group_folder = os.path.join(os.getcwd(), 'pages', group)
            os.makedirs(group_folder, exist_ok=True)
            for page in pages:
                page_path = os.path.join(group_folder, f"{page}.mdx")
                with open(page_path, 'w') as page_file:
                    template_header = generate_template_header(page_path)
                    page_file.write(template_header +
                                    "\n\nContent for {page} page.")


def generate_template_header(file_path):
    """
    Generates a template header for a given file path.

    :param file_path: The path of the file.
    :return: A string containing the template header.
    """
    # Extract the file name from the path
    file_name = os.path.basename(file_path)
    # Remove the file extension
    title = file_name.replace('_', ' ').rsplit('.', 1)[0].title()

    print("Generate template file header for", file_path)

    # Extract API endpoints from the Rust file
    api_endpoints = extract_endpoints_from_rs_file(file_path)
    api_endpoint = api_endpoints[
        0] if api_endpoints else "GET /endpoint-unavailable"

    template_header = f"""---\ntitle: '{title}'\napi: '{api_endpoint}'\n---"""


    return template_header
