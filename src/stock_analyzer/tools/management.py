import json
import logging
import time
from typing import Iterable

from openai.types.beta.threads import RequiredActionFunctionToolCall
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

from stock_analyzer.tools.definitions import available_functions

logger = logging.getLogger(__name__)

def process_tool_calls(
        tool_calls: list[RequiredActionFunctionToolCall]) -> Iterable[ToolOutput]:
    output: list[ToolOutput] = []
    for call in tool_calls:
        logger.info(f"Tool call with ID and name: {call.id}, {call.function.name}")
        start_time: float = time.perf_counter()
        function_name: str = call.function.name
        function_args: dict = json.loads(call.function.arguments)
        response = available_functions().get(function_name)(**function_args)
        time_series: str = json.dumps(response[list(response.keys())[1]])
        output.append(
            {
                "tool_call_id": call.id,
                "output": time_series
            }
        )
        logger.info(f"Done! response received in {time.perf_counter() - start_time:.6f} s")
    return output