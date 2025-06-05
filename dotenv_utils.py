from os import getenv
from dotenv import load_dotenv

def get_dotenv_variable_or_exception(key: str):
    load_dotenv()
    value = getenv(f"API_KEY_{key.upper()}")
    print(value)
    if not value:
        raise ValueError("This model is not implemented yet")
    return value