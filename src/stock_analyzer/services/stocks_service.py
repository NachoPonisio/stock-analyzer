from typing import Literal, Any

import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

from stock_analyzer.config import get_config, AppConfig

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def retrieve_time_series(symbol: str, interval: Literal["intraday", "daily", "weekly", "monthly"]) -> dict[str, Any]:
    config: AppConfig = get_config()
    api_key: str = config.alphavantage_api_key
    base_url: str = config.alphavantage_base_url

    interval_to_function: dict[str, str] = {
        "intraday": "TIME_SERIES_INTRADAY",
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }
    
    function: str | None = interval_to_function.get(interval)
    if not function:
        raise RuntimeError(f"Invalid interval: {interval}")

    url: str = f"{base_url}?function={function}&symbol={symbol}&apikey={api_key}"
    if interval == "intraday":
        url += "&interval=5min"

    response: requests.Response = requests.get(url)
    response.raise_for_status()
    return response.json()
