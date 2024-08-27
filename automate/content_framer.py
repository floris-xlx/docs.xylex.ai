from automate.prompt_gpt_openai import prompt_openai_model

import json
import os

async def update_mdx_files_with_parameters(file_list):
    for file_info in file_list:
        mdx_filepath = file_info['mdx_filepath']
        file_path = file_info['file_path']

        # Read the Rust file content
        try:
            with open(file_path, 'r') as rust_file:
                rust_content = rust_file.read()
        except FileNotFoundError:
            print(f"Rust file not found: {file_path}")
            continue

        # Extract parameters from the Rust file
        parameters = extract_parameters_from_rust(rust_content)

        # Format parameters for MDX
        param_fields = format_parameters_for_mdx(parameters)

        # Read the existing MDX file content
        try:
            with open(mdx_filepath, 'r') as mdx_file:
                mdx_content = mdx_file.read()
        except FileNotFoundError:
            print(f"MDX file not found: {mdx_filepath}")
            continue

        # Insert the parameter fields into the MDX content
        updated_mdx_content = insert_parameters_into_mdx(mdx_content, param_fields)

        # Write the updated content back to the MDX file
        with open(mdx_filepath, 'w') as mdx_file:
            mdx_file.write(updated_mdx_content)

        print(f"Updated MDX file: {mdx_filepath}")

def extract_parameters_from_rust(rust_content):
    # This function should parse the Rust content and extract parameters
    # For simplicity, let's assume it returns a list of parameter names
    # In a real implementation, you would parse the Rust code to find parameters
    return ["param1", "param2"]  # Example parameters

def format_parameters_for_mdx(parameters):
    # Format the parameters for MDX
    param_fields = ""
    for param in parameters:
        param_fields += f'<ParamField path="{param}" type="string">\n  An example of a parameter field\n</ParamField>\n'
    return param_fields

def insert_parameters_into_mdx(mdx_content, param_fields):
    # Insert the parameter fields into the MDX content
    # Assuming we insert after the header
    header_end_index = mdx_content.find('---', mdx_content.find('---') + 1) + 3
    return mdx_content[:header_end_index] + "\n" + param_fields + mdx_content[header_end_index:]


