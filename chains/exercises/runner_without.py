# chains/exercises/runner_without.py
import asyncio
from typing import AsyncGenerator
from config.llm_config import llms
from config.chain_configs import chain_configs
from config.templates import template_sanitize_fluster


# chains/exercises/runner_utils.py (for example)

import asyncio
from typing import Tuple, Any
from langchain_core.prompts.chat import ChatPromptTemplate

async def write_fluster_track(
    track_index: int,
    user_input_text: str,
    template_write_a: ChatPromptTemplate,
    template_write_b: ChatPromptTemplate,
    llm_a: Any,
    llm_b: Any,
    # If you later enable the "refine" step, pass those too:
    # template_refine: ChatPromptTemplate,
    # llm_refine: Any,
    template_sanitize: ChatPromptTemplate,
    llm_sanitize: Any
) -> Tuple[int, str]:
    """
    A reusable helper that:
      (1) Picks prompt A or B,
      (2) Picks LLM A or B,
      (3) Generates a fluster,
      (4) Optionally refines distractors,
      (5) Sanitizes,
      (6) Returns (track_index, final_text).
    """

    # Decide which prompt to use
    if track_index in (0, 2):
        gen_template = template_write_a
    else:
        gen_template = template_write_b

    # Decide which LLM to use
    if track_index in (0, 1):
        gen_llm = llm_a
    else:
        gen_llm = llm_b

    # 1) Generate
    gen_msg = await gen_template.aformat_prompt(learning_objective=user_input_text)
    gen_resp = await gen_llm.ainvoke(gen_msg.to_messages())
    write_fluster_result = getattr(gen_resp, "content", gen_resp)

    # 2) Refine distractors (currently skipped)
    # refine_msg = await template_refine.aformat_prompt(write_fluster_result=write_fluster_result)
    # refine_resp = await llm_refine.ainvoke(refine_msg.to_messages())
    # refined_output = getattr(refine_resp, "content", refine_resp)

    # 3) Sanitize
    sanitize_msg = await template_sanitize.aformat_prompt(refinement_result=write_fluster_result)
    sanitize_resp = await llm_sanitize.ainvoke(sanitize_msg.to_messages())
    sanitized_output = getattr(sanitize_resp, "content", sanitize_resp)

    return (track_index, sanitized_output)


async def run_fluster_no_diagnosis(
    user_input_text: str,
    model_choice_1: str,  # for "LLM A"
    model_choice_2: str   # for "LLM B"
) -> AsyncGenerator[tuple, None]:
    """
    Generates exercises in 4 parallel tracks:
      - (Prompt A, LLM A), (Prompt B, LLM A), (Prompt A, LLM B), (Prompt B, LLM B)
    Then refines distractors, then sanitizes.
    Yields partial updates (4 textboxes) as each track completes.
    """

    # Get the chain config
    config = chain_configs["fluster"]

    # Extract the chain object fields
    template_write_a = config["template_write_fluster_a"]
    template_write_b = config["template_write_fluster_a"]

    # pick the LLMs based on user input or the default from config
    llm_a = llms.get(model_choice_1, config["default_llm_a"])
    llm_b = llms.get(model_choice_2, config["default_llm_b"])

    # we skip refinement for now
    # template_refine = config["template_refine_fluster"]
    # llm_refine = config["llm_refine"]

    template_sanitize = config["template_sanitize"]
    llm_sanitize = config["llm_sanitize"]

    # We'll hold the final results for each of the 4 tracks in a list
    partial_results = ["", "", "", ""]

    ## We'll define tasks that each call `write_fluster_track(...)`
    tasks = []
    for track_i in range(4):
        coro = write_fluster_track(
            track_i,
            user_input_text,
            template_write_a,
            template_write_b,
            llm_a,
            llm_b,
            template_sanitize,
            llm_sanitize
        )
        tasks.append(coro)


    # Run them in parallel
    for coro in asyncio.as_completed(tasks):
        track_idx, final_text = await coro
        partial_results[track_idx] = final_text

        # Yield partial update (4-tuple). The UI will map each item to a separate textbox.
        yield tuple(partial_results)
