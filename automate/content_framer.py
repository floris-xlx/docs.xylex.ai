from automate.prompt_gpt_openai import prompt_openai_model, prompt_openai_model_endpoint

import json
import os


def endpoint_description_gen(rust_content, endpoint):
    prompt = f"Describe this Rust endpoint max 3 sentences and ONLY describe this endpoint {endpoint}: \n\n" + rust_content
    return prompt_openai_model_endpoint(prompt)


async def update_mdx_files_with_parameters(file_list):
    for file_info in file_list:
        mdx_filepath = file_info['mdx_filepath']
        file_path = file_info['file_path']

        # Read the Rust file content
        try:
            with open(file_path, 'r') as rust_file:
                rust_content = rust_file.read()
        except FileNotFoundError:
            print(f"\033[91mRust file not found: {file_path}\033[0m")
            continue

        # Extract parameters from the Rust file
        parameters = extract_parameters_from_rust(rust_content)

        endpoint = file_info['endpoint']
        endpoint_description = endpoint_description_gen(rust_content, endpoint)

        # Format parameters for MDX
        param_fields = format_parameters_for_mdx(parameters)

        # Read the existing MDX file content
        try:
            with open(mdx_filepath, 'r') as mdx_file:
                mdx_content = mdx_file.read()
        except FileNotFoundError:
            print(f"\033[91mMDX file not found: {mdx_filepath}\033[0m")
            continue

        # Insert the endpoint description into the MDX content
        mdx_content_with_desc = format_endpoint_description(
            mdx_content, endpoint_description)

        # Insert the parameter fields into the MDX content
        updated_mdx_content = insert_parameters_into_mdx(
            mdx_content_with_desc, param_fields)

        # Write the updated content back to the MDX file
        with open(mdx_filepath, 'w') as mdx_file:
            mdx_file.write(updated_mdx_content)

        print(f"\033[93mUpdated MDX file: {mdx_filepath}\033[0m")


def extract_parameters_from_rust(rust_content):
    # Use the prompt_openai_model to extract parameters from the Rust content
    print("\033[94mExtracting parameters from Rust endpoints...\033[0m")

    prompt = "Extract the parameters from the following Rust content, usually they will be in the struct:\n\n"
    parameters = prompt_openai_model(prompt + rust_content)

    if parameters is not None:
        parameters = parameters.replace("```json", "").replace("```",
                                                               "").strip()
    else:
        parameters = ""
    print("Extracted parameters:", parameters)

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
    added_names = set()
    for param in parameters:
        if param["name"] != "cache" and param["name"] not in added_names:
            param_fields += f'<ParamField query="{param["name"]}" type="{param["type"]}" {"required " if param["required"] else ""} children="{param["text_explanation_long"]}">\n  {param["text_explanation_short"]}\n</ParamField>\n'
            added_names.add(param["name"])

    return param_fields


def insert_parameters_into_mdx(mdx_content, param_fields):
    print("\033[94mInserting parameters into MDX content...\033[0m")
    print("MDX content:", mdx_content)
    print("Parameter fields:", param_fields)
    # Just paste it under the existing content with 4 new lines above
    return mdx_content + "\n\n\n\n" + param_fields


def format_endpoint_description(mdx_content, description):
    if "endpoint_description" in description and len(description["endpoint_description"]) > 3:
        description = f'<Card title="Endpoint Description" icon="info" horizontal >{description["endpoint_description"]}</Card>\n\n'

        # Just paste it under the existing content with 4 new lines above
        return mdx_content + "\n\n\n\n" + description
    return mdx_content
