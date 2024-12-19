import os
import yaml
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Load configuration from YAML file
with open('auto-generate-config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extract necessary configuration values
open_ai_model = config['open_ai']['open_ai_model']
open_ai_max_tokens = config['open_ai']['open_ai_max_tokens']
open_ai_temperature = config['open_ai']['open_ai_temperature']
open_ai_key = os.getenv(config['env']['open_ai_key'])

# Initialize OpenAI client and set API key
client = OpenAI(api_key=open_ai_key)



def prompt_openai_model(prompt_text):
    """
    Prompts the OpenAI model with the given text and returns the response.

    :param prompt_text: The text to prompt the model with.
    :return: The response from the OpenAI model.
    """
    response = client.chat.completions.create(
        model=open_ai_model,
        messages=[{
            "role":
            "system",
            "content":
            "Only respond with a list with parameters (also anytime a query struct is passed into the rust function parameters you can assume those are also parameters from the struct defintion so take those too but dont duplicate) with keys: name, type, required(bool), text_explanation_short, text_explanation_long"
        }, {
            "role": "user",
            "content": prompt_text
        }],
        max_tokens=open_ai_max_tokens,
        temperature=open_ai_temperature)
    return response.choices[0].message.content

import json


def prompt_openai_model_endpoint(prompt_text):
    """
    Prompts the OpenAI model with the given text and returns the response.

    :param prompt_text: The text to prompt the model with.
    :return: The response from the OpenAI model.
    """
    response = client.chat.completions.create(
        model=open_ai_model,
        messages=[{
            "role":
            "system",
            "content":
            "MAX 250 CHARACTERS Describe this rust endpoint and only respond VERY concise, Dont talk about Rust endpoint, GET or POST, the ROute, just the description of the endpoint"
        }, {
            "role": "user",
            "content": prompt_text
        }],
        max_tokens=open_ai_max_tokens,
        temperature=open_ai_temperature)
    message = response.choices[0].message.content

    # replace any " or ' with `
    if message is None:
        message = ""
    else:
        message = message.replace('"', '`').replace("'", '`')

    if message:
        return {"endpoint_description": message}
    else:
        return {"endpoint_description": ""}
