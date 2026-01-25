from typing import Callable

from openai.types.beta.assistant_tool_param import AssistantToolParam

from stock_analyzer.services.stocks_service import retrieve_time_series


def available_tools() -> list[AssistantToolParam]:
    functions_list: list[AssistantToolParam] = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_time_series",
                "description": "Retrieves information for a certain stock symbol, for different time intervals represented by the `interval` parameter",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "The stock symbol from which information is requested"},
                        "interval": {
                            "type": "string",
                            "description": "The time interval for which information is requested. Accepts the following values: 'intraday', 'daily', 'weekly', 'monthly'"},
                    },
                    "required": ["symbol", "interval"],
                },
            },
        },
        {
            "type": "code_interpreter"
        }
    ]
    return functions_list

def available_functions() -> dict[str, Callable] :
    return {
        "retrieve_time_series": retrieve_time_series
    }
