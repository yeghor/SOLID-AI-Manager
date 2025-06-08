from os import getenv
from dotenv import load_dotenv

def get_dotenv_api_key_or_exception(key: str):
    load_dotenv()
    value = getenv(f"API_KEY_{key.upper()}")
    if not value:
        raise ValueError("This model is not implemented yet. DOTENV")
    return value