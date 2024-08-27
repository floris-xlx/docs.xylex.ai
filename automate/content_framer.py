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
    # Use the prompt_openai_model to extract parameters from the Rust content
    print("Extracting parameters from Rust content...")
    print(rust_content)

    prompt = "Extract the parameters from the following Rust content, usually they will be in the struct:\n\n"
    parameters = prompt_openai_model(prompt + rust_content)

    print("Extracted parameters:")
    print(parameters)

    if parameters is not None:
        parameters = parameters.replace("```json", "").replace("```", "").strip()
    else:
        parameters = ""
    # Parse the extracted parameters
    try:
        # Attempt to parse the JSON string into a Python object
        parameters_list = json.loads(parameters)
    except (TypeError, json.JSONDecodeError):
        # If there's an error in decoding, print an error message and return an empty list
        print("Failed to decode JSON parameters or parameters is None.")
        return []
    return parameters_list

def format_parameters_for_mdx(parameters):
    # Format the parameters for MDX
    param_fields = ""
    for param in parameters:
        param_fields += f'<ParamField name="{param["name"]}" type="{param["type"]}">\n  An example of a parameter field\n</ParamField>\n'
    return param_fields


def insert_parameters_into_mdx(mdx_content, param_fields):
    # Just paste it under the existing content with 4 new lines above
    return mdx_content + "\n\n\n\n" + param_fields
