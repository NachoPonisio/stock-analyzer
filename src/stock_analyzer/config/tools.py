import os
from typing import Optional

from dotenv import load_dotenv


def load_configs() -> tuple[str, str, str, bool]:
    load_dotenv()
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not api_key: raise EnvironmentError("OPENAI_API_KEY not present")
    delete_if_existent: bool = bool(os.getenv("DELETE_ASSISTANT_IF_EXISTS"))
    return os.getenv("ASSISTANT_NAME"), os.getenv("ASSISTANT_INSTRUCTIONS"), api_key, delete_if_existent
