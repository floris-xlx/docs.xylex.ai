import os
from automate.parse_api_endpoint import extract_http_methods_from_rs_file
from automate.index_nav_groups import generate_template_header
import json


def create_mdx_file_if_not_exists(mdx_filepath, parent_folder_name, endpoint):
    if not os.path.exists(mdx_filepath):
        template_header = generate_template_header(parent_folder_name,
                                                   endpoint)
        with open(mdx_filepath, 'w') as mdx_file:
            mdx_file.write(template_header)


def find_and_extract_endpoints():
    base_path = 'cache/api'
    endpoints = []

    for root, dirs, files in os.walk(base_path):
        if 'endpoint.rs' in files:
            file_path = os.path.join(root, 'endpoint.rs')
            parent_folder_name = os.path.basename(root)
            extracted_endpoints = extract_http_methods_from_rs_file(file_path)
            if extracted_endpoints:
                for endpoint in extracted_endpoints:

                    mdx_filepath = f"{root.replace('cache/api', 'pages')}.mdx"
                    create_mdx_file_if_not_exists(mdx_filepath,
                                                  parent_folder_name, endpoint)
                    endpoints.append({
                        "endpoint":
                        endpoint,
                        "file_path":
                        file_path,
                        "parent_folder":
                        parent_folder_name,
                        "pages_folder":
                        root.replace('cache/api', 'pages'),
                        "mdx_filepath":
                        mdx_filepath
                    })

    return endpoints


if __name__ == '__main__':
    endpoints = find_and_extract_endpoints()
    print(json.dumps(endpoints, indent=4))
