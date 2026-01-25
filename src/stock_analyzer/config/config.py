import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    assistant_name: Optional[str]
    assistant_instructions: Optional[str]
    openai_api_key: str
    alphavantage_api_key: str
    alphavantage_base_url: str
    delete_if_exists: bool


@lru_cache()
def get_config() -> AppConfig:
    load_dotenv()
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not present")

    alphavantage_api_key: Optional[str] = os.getenv("ALPHAVANTAGE_API_KEY")
    if not alphavantage_api_key:
        raise RuntimeError("ALPHAVANTAGE_API_KEY not present")

    alphavantage_base_url: Optional[str] = os.getenv("ALPHAVANTAGE_BASE_URL")
    if not alphavantage_base_url:
        raise RuntimeError("ALPHAVANTAGE_BASE_URL not configured")
    delete_if_existent: bool = os.getenv("DELETE_IF_EXISTS", "False").lower() == "true"

    return AppConfig(
        assistant_name=os.getenv("ASSISTANT_NAME"),
        assistant_instructions=os.getenv("ASSISTANT_INSTRUCTIONS"),
        openai_api_key=openai_api_key,
        alphavantage_api_key=alphavantage_api_key,
        alphavantage_base_url=alphavantage_base_url,
        delete_if_exists=delete_if_existent
    )
