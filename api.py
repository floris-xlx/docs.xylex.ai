from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class APIKeyHeader(BaseModel):
    api_key: str


def get_api_key(api_key_header: APIKeyHeader):
    load_dotenv()

    api_key = os.getenv("XLX_DOCS_XYLEX_API_KEY")
    if api_key_header.api_key != api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key_header.api_key

@app.get("/build-docs")
async def build_docs(api_key: str):
    api_key = get_api_key(APIKeyHeader(api_key=api_key))
    return {"message": "Building docs..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3398)
