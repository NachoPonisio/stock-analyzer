import time
from typing import Iterable

from openai import OpenAI
from openai.types.beta.assistant import Assistant

from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run
from openai.types.beta.threads.message import Message

from stock_analyzer.assistants import get_or_create_assistant
from stock_analyzer.assistants.tools import ONGOING_STATUSES, iterate_run
from stock_analyzer.config import load_configs
from stock_analyzer.tools.definitions import available_tools


def execute () -> None:
    """
    Main entry point for the stock analyzer application.
    """
    assistant_name, assistant_instructions, api_key, delete_if_exists = load_configs()
    client: OpenAI = OpenAI(api_key=api_key)
    assistant: Assistant = get_or_create_assistant(
        client=client,
        name=assistant_name,
        instructions=assistant_instructions,
        tools=available_tools(),
        delete_if_exists=delete_if_exists
    )

    thread: Thread = client.beta.threads.create()
    message: Message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Retrieve and show the latest daily time series data for the stock symbol 'AAPL'."
    )

    run: Run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )


    while run.status not in ONGOING_STATUSES:
        run = iterate_run(client, run_id=run.id, thread_id=thread.id)

    messages: Iterable[Message] = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in messages:
        if message.role == "assistant":
            print(f"Assistant: {message.content[0].text.value}")



