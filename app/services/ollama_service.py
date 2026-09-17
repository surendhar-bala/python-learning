import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/chat"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def extract_company_info(web_content: str):

    prompt = f"""
Extract company information.

Rules:
- Use ONLY the supplied content.
- Do not hallucinate.
- Return valid JSON.

Fields:
legal_name
website
industry
description
headquarters

Content:
{web_content}
"""

    schema = {
        "type": "object",
        "properties": {
            "legal_name": {"type": ["string", "null"]},
            "website": {"type": ["string", "null"]},
            "industry": {"type": ["string", "null"]},
            "description": {"type": ["string", "null"]},
            "headquarters": {"type": ["string", "null"]}
        },
        "required": [
            "legal_name",
            "website",
            "industry",
            "description",
            "headquarters"
        ]
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "format": schema
    }

    print("Ollama URL:", OLLAMA_URL)
    print("Ollama model:", MODEL)

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return json.loads(
        result["message"]["content"]
    )