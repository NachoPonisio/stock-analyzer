# Configuring

In your `.env` file, configure:

```dotenv
OPENAI_API_KEY="<<YOUR_OPENAI_API_KEY>>"
ASSISTANT_NAME="stock_analyzer_assistant"
ASSISTANT_INSTRUCTIONS="You're an experienced stock analyzer assistant tasked with analyzing and visualizing stock market data."

```

# Installing and running.

`poetry.lock` and `pyproject.toml` should be available in the root of the project structure, unless I forgot to add them :sweat_smile:

Run `poetry install` and `poetry run stock_analyzer`.