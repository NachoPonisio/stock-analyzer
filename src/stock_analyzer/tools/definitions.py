def available_tools() -> list[dict]:
    functions_list = [
        {
            "type": "function",
            "function": {
                "name": "get_time_series",
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
        }
    ]
    return functions_list
