import os
import time
from typing import Iterable, Final, Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run
from openai.types.beta.threads.message import Message


def get_or_create_assistant(client: OpenAI, name: str, instructions: str, model: str = "gpt-4o") -> Assistant:
    """Finds an existing assistant by name or creates a new one."""
    existing_assistants: Iterable[Assistant] = client.beta.assistants.list()
    assistant: Optional[Assistant] = next((a for a in existing_assistants if a.name == name), None)

    if assistant:
        print(f"Matching `{name}` assistant found, using the first matching assistant with ID: {assistant.id}")
        return assistant
    else:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model
        )
        print(f"No matching `{name}` found, creating a new assistant with ID: {assistant.id}")

        return assistant


def execute () -> None:
    """
    Main entry point for the stock analyzer application.
    """
    load_dotenv()
    assistant_name: Final = os.getenv("ASSISTANT_NAME")
    assistant_instructions: Final = os.getenv("ASSISTANT_INSTRUCTIONS")
    api_key: Final = os.getenv("OPENAI_API_KEY")

    client: OpenAI = OpenAI(api_key=api_key)
    assistant: Assistant = get_or_create_assistant(client, assistant_name, assistant_instructions)
    thread: Thread = client.beta.threads.create()
    message: Message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Tell me your name and instructions. YOU MUST Provide a DIRECT and SHORT response."
    )

    run: Run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status != "completed":
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {run.status}")

    messages: Iterable[Message] = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in messages:
        if message.role == "assistant":
            print(f"Assistant: {message.content[0].text.value}")
