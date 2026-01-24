import logging
import time
from typing import Iterable

from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run, RequiredActionFunctionToolCall
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

from stock_analyzer.assistants import get_or_create_assistant
from stock_analyzer.assistants import iterate_run
from stock_analyzer.config import get_config, AppConfig
from stock_analyzer.tools import process_tool_calls
from stock_analyzer.tools.definitions import available_tools

logging.basicConfig(level=logging.INFO)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.ERROR)

logger = logging.getLogger(__name__)

def execute() -> None:
    """
    Main entry point for the stock analyzer application.
    """
    start_time: float = time.perf_counter()
    config: AppConfig = get_config()
    client: OpenAI = OpenAI(api_key=config.openai_api_key)
    assistant: Assistant = get_or_create_assistant(
        client=client,
        name=config.assistant_name,
        instructions=config.assistant_instructions,
        tools=available_tools(),
        delete_if_exists=config.delete_if_exists
    )

    thread: Thread = client.beta.threads.create()
    logger.info(f"Thread created with ID: {thread.id}")
    message: Message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Retrieve and show the latest daily time series data for the stock symbol 'AAPL'."
    )

    run: Run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = iterate_run(client, run_id=run.id, thread_id=thread.id)

    logger.info(f"Run initiated with ID: {run.id}")
    logger.info(f"Waiting for response from `{assistant.name}`. Elapsed time: {time.perf_counter() - start_time:.6f} s")

    if run.status == "requires_action":
        tool_calls: list[RequiredActionFunctionToolCall] = run.required_action.submit_tool_outputs.tool_calls
        outputs: Iterable[ToolOutput] = process_tool_calls(tool_calls)
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=outputs
        )
        run = iterate_run(client, run_id=run.id, thread_id=thread.id)
        logger.info(f"Run initiated with ID: {run.id}")


    messages: Iterable[Message] = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    for message in messages:
        if message.role == "assistant":
            logger.info(f"Assistant: {message.content[0].text.value}")

if __name__ == "__main__":
    execute()