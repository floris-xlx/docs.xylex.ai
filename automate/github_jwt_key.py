#!/usr/bin/env python3
import sys
import time

import jwt

from dotenv import load_dotenv
import os

load_dotenv()

# Get PEM file path from environment variable
pem = os.getenv('XLX_DOCS_BUILD_PACK_TOKEN_PATH')
client_id = os.getenv('XLX_DOCS_GITHUB_APP_CLIENT_ID')
if not client_id:
    raise ValueError("GitHub App Client ID is not set in the environment variable.")
# Open PEM


if pem is not None:
    with open(pem, "rb") as pem_file:
        signing_key = pem_file.read()
else:
    raise ValueError("PEM file path is not set in the environment variable.")

payload = {
    # Issued at time
    "iat": int(time.time()),
    # JWT expiration time (10 minutes maximum)
    "exp": int(time.time()) + 600,
    # GitHub App's client ID
    "iss": client_id,
}

# Create JWT
encoded_jwt = jwt.encode(payload, signing_key, algorithm="RS256")

def generate_jwt():
    return encoded_jwt