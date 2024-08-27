import os
import re


def print_colored(message, color_code):
    print(f"\033[{color_code}m{message}\033[0m")


def extract_endpoints_from_rs_file(file_path):
    print_colored(f"Original file path: {file_path}", '34')  # Blue

    if file_path.startswith('/'):
        file_path = f".{file_path}"
        print_colored(f"Adjusted file path for leading slash: {file_path}",
                      '33')  # Yellow

    if not file_path.endswith('.mdx'):
        print_colored("File path does not end with '.mdx'. Returning None.",
                      '31')  # Red
        return None

    file_path = re.sub(r'.*/pages/', '/cache/api/',
                       file_path).replace('.mdx', '.rs')
    print_colored(f"Transformed file path: {file_path}", '32')  # Green

    if os.path.exists(f'.{file_path}') or os.path.exists(file_path):
        actual_path = f'.{file_path}' if os.path.exists(
            f'.{file_path}') else file_path
        print_colored(f"File exists: {actual_path}", '32')  # Green
        return extract_http_methods_from_rs_file(actual_path)

    directory_path = file_path.replace('.rs', '')
    if os.path.isdir(directory_path):
        file_path = os.path.join(directory_path, 'endpoint.rs')
        print_colored(f"Directory exists, adjusted file path: {file_path}",
                      '33')  # Yellow
        return extract_http_methods_from_rs_file(file_path)

    print_colored("File or directory does not exist. Returning None.",
                  '31')  # Red
    return None


def extract_http_methods_from_rs_file(file_path):
    """
    Extracts HTTP methods and their paths from a Rust file.

    :param file_path: The path of the Rust file.
    :return: A list of formatted endpoint strings.
    """
    if not file_path:
        print_colored("No file path provided. Returning empty list.",
                      '31')  # Red
        return []

    print_colored(f"Extracting HTTP methods from file: {file_path}",
                  '34')  # Blue

    endpoints = []
    start_pattern = r'#\[(get|put|post|delete|head)\("/'
    end_pattern = r'"\)\]'

    try:
        with open(file_path, 'r') as file:
            print_colored(f"Opened file: {file_path}", '32')  # Green
            content = file.read()
            matches = re.findall(f'{start_pattern}(.*?){end_pattern}', content,
                                 re.IGNORECASE)
            print_colored(f"Found {len(matches)} matches in the file.",
                          '32')  # Green
            for method, path in matches:
                endpoint = f"{method.upper()} https://api.v2.xylex.ai/{path}"
                print_colored(f"Extracted endpoint: {endpoint}", '34')  # Blue
                endpoints.append(endpoint)
    except FileNotFoundError:
        print_colored(f"File not found: {file_path}", '31')  # Red
    except Exception as e:
        print_colored(f"An error occurred: {str(e)}", '31')  # Red

    print_colored(f"Total endpoints extracted: {len(endpoints)}", '34')  # Blue
    return endpoints
