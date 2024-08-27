import os
import json

def sync_nav_tags():
    pages_dir = './pages'
    mint_file = 'mint.json'

    # Load the existing mint.json data
    with open(mint_file, 'r') as file:
        mint_data = json.load(file)

    # Create a dictionary to hold the new navigation structure
    new_navigation = []

    # Iterate through each folder in the pages directory
    for folder in os.listdir(pages_dir):
        folder_path = os.path.join(pages_dir, folder)
        if os.path.isdir(folder_path):
            group_key = f"{folder.capitalize()} API" if folder.lower() != 'organization' else folder.capitalize()
            pages = []

            # Iterate through each .mdx file in the subfolder
            for subfile in os.listdir(folder_path):
                if subfile.endswith('.mdx'):
                    page_entry = f"pages/{folder}/{subfile.replace('.mdx', '')}"
                    pages.append(page_entry)

            # Only add or update the group if pages is not empty
            if pages:
                group_exists = False
                for nav_group in mint_data['navigation']:
                    if nav_group['group'] == group_key:
                        nav_group['pages'] = pages
                        group_exists = True
                        break

                if not group_exists:
                    new_navigation.append({
                        "group": group_key,
                        "pages": pages
                    })

    # Add new groups to the existing navigation
    mint_data['navigation'].extend(new_navigation)

    # Save the updated mint.json data
    with open(mint_file, 'w') as file:
        json.dump(mint_data, file, indent=4)

# Call the function to sync navigation tags
sync_nav_tags()
