# Changes from TASK #1
- Incorporated feedback about config management, it is now encapsulated in a separate module.
- Incorporated feedback about the assistant creation process, it is encapsulated under the `assistants` module
- Incorporated feedback about management of different run states. The logic was enhanced and abstracted under the `assistants` module, `iterate_run` function.
- Included logginggit

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