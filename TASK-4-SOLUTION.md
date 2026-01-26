# Changes from TASK #3
- Added logic to fetch `image_file` content type

# Configuring

In your `.env` file, configure:

```dotenv
OPENAI_API_KEY="<<YOUR_OPENAI_API_KEY>>"
ASSISTANT_NAME="stock_analyzer_assistant"
ASSISTANT_INSTRUCTIONS="You're an experienced stock analyzer assistant tasked with analyzing and visualizing stock market data."
ALPHAVANTAGE_API_KEY="<<YOUR_ALPHAVANTAGE_API_KEY>>"
ALPHAVANTAGE_BASE_URL=https://www.alphavantage.co/query
DELETE_IF_EXISTS="false" #If set to true, It will delete any assistant named ASSISTANT_NAME on startup
```

# Installing and running.

`poetry.lock` and `pyproject.toml` should be available in the root of the project structure, unless I forgot to add them :sweat_smile:

Run `poetry install` and `poetry run stock_analyzer`.