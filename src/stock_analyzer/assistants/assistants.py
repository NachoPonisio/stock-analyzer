import logging
import time
from typing import Iterable, Optional, Final

from openai import OpenAI
from openai.types.beta import Assistant
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai.types.beta.threads import Run

logger = logging.getLogger(__name__)

ONGOING_STATUSES: Final = ["queued", "in_progress", "cancelling"]
RETURN_STATUSES: Final = ["requires_action", "completed"]
FAILURE_STATUSES: Final = ["cancelled", "failed", "incomplete", "expired"]

def get_or_create_assistant(
        client: OpenAI,
        name: str,
        instructions: str,
        tools: Iterable[AssistantToolParam],
        model: str = "gpt-4.1-nano",
        delete_if_exists: bool = False) -> Assistant:

    """Finds an existing assistant by name or creates a new one."""
    existing_assistants: Iterable[Assistant] = client.beta.assistants.list()
    assistant: Optional[Assistant] = next((a for a in existing_assistants if a.name == name), None)

    if assistant:
        if delete_if_exists:
            client.beta.assistants.delete(assistant_id=assistant.id)
            assistant: Assistant = client.beta.assistants.create(
                    name=name,
                    instructions=instructions,
                    model=model,
                    tools=tools

                )
            logger.info(f"Matching `{name}` assistant found and `delete_if_exists` flag set to True, deleting and creating new assistant: {assistant.id}")
            return assistant

        logger.info(f"Matching `{name}` assistant found, using the first matching assistant with ID: {assistant.id}")
        return assistant
    else:
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools
        )
        logger.info(f"No matching `{name}` found, creating a new assistant with ID: {assistant.id}")
        return assistant



def iterate_run(client: OpenAI, run_id: str, thread_id: str) -> Run | None:
    time.sleep(1)
    run: Run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )

    match run.status:
        case o if o in ONGOING_STATUSES:
            return iterate_run(client=client, run_id=run_id, thread_id=thread_id)
        case r if r in RETURN_STATUSES:
            return run
        case f if f in FAILURE_STATUSES:
            raise RuntimeError(f"Thread finished with an unexpected status: {f}")






