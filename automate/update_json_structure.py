import os
import json

def load_mint_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_mint_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def get_mdx_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.mdx')]

def update_group_pages(group, base_path, ignore_folders):
    group_path = os.path.join(base_path, group['group'].lower()).replace("\\", "/")
    if os.path.isdir(group_path) and group['group'].lower() not in ignore_folders:
        mdx_files = get_mdx_files(group_path)
        group['pages'] = [os.path.join(group['group'].lower(), f).replace("\\", "/").replace('.mdx', '') for f in mdx_files]

def update_navigation():
    ignore_folders = {'images', 'logo', 'snippets'}
    base_path = os.getcwd()
    mint_data = load_mint_data('mint.json')

    for group in mint_data['navigation']:
        if group['group'] != 'Get Started':
            update_group_pages(group, base_path, ignore_folders)

    save_mint_data('mint.json', mint_data)






if __name__ == '__main__':
    update_navigation()
