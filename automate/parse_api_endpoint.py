import os
import re


def extract_endpoints_from_rs_file(file_path):

    def print_colored(message, color_code):
        print(f"\033[{color_code}m{message}\033[0m")

    print_colored(f"Original file path: {file_path}", '34')  # Blue

    if file_path.startswith('/'):
        file_path = f".{file_path}"
        print_colored(f"Adjusted file path for leading slash: {file_path}",
                      '33')  # Yellow

    if not file_path.endswith('.mdx'):
        print_colored("File path does not end with '.mdx'. Returning None.",
                      '31')  # Red
        return None

    match = re.search(r'.*/pages/', file_path)
    if match:
        file_path = file_path.replace(match.group(), '/cache/api/')
        print_colored(f"Replaced '/pages/' with '/cache/api/': {file_path}",
                      '32')  # Green
    file_path = file_path.replace('.mdx', '.rs')

    print_colored(f"Replaced '.mdx' with '.rs': {file_path}", '32')  # Green
    if os.path.exists(f'.{file_path}') or os.path.exists(file_path):
        print_colored(f"File exists: {file_path}", '32')  # Green
    else:
        print_colored(f"File does not exist: {file_path}", '31')  # Red
        directory_path = file_path.replace('.rs', '')
        if os.path.isdir(directory_path):
            file_path = os.path.join(directory_path, 'endpoint.rs')
            print_colored(f"Directory exists, adjusted file path: {file_path}",
                          '33')  # Yellow
        else:
            print_colored("Directory does not exist. Returning None.",
                          '31')  # Red
            return None

    print_colored(f"Final file path: {file_path}", '34')  # Blue
    return file_path
