import logging
import tempfile
import time
from typing import Iterable

from openai import OpenAI, HttpxBinaryResponseContent
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Run, RequiredActionFunctionToolCall
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from openai.types.beta.threads.runs import RunStep

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
        content="Retrieve the monthly time series data for the stock symbol 'CRM' for the latest 3 months. Analyze the retrieved stock data and identify any trends, calculate ratios, key metrics, etc. Limit your responses to a text summary."
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
            block = message.content[0]

            match block.type:
                case "text":
                    logger.info("Assistant: %s", block.text.value)
                case "image_file":
                    file_id = block.image_file.file_id
                    file_contents: HttpxBinaryResponseContent = client.files.content(file_id=file_id)
                    with tempfile.NamedTemporaryFile(delete=False, mode='wb', suffix='.png') as temp_file:
                        temp_file.write(file_contents.read())
                        logger.info(f"Assistant: Generated temporary file at {temp_file.name}")

    steps: Iterable[RunStep] = client.beta.threads.runs.steps.list(
        run_id=run.id,
        thread_id=thread.id
    )

    for step in steps:
        logger.info(f"Steps: {step.id}, type: {step.type}, status: {step.status}")

if __name__ == "__main__":
    execute()