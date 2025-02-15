# chains/exercises/runner.py
import asyncio
from typing import AsyncGenerator
from config.llm_config import llms
from config.chain_configs import chain_configs

async def run_fluster(
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
    template_write_b = config["template_write_fluster_b"]

    # pick the LLMs based on user input or the default from config
    llm_a = llms.get(model_choice_1, config["default_llm_a"])
    llm_b = llms.get(model_choice_2, config["default_llm_b"])

    template_refine = config["template_refine_fluster"]
    llm_refine = config["llm_refine"]

    template_sanitize = config["template_sanitize"]
    llm_sanitize = config["llm_sanitize"]

    # We'll hold the final results for each of the 4 tracks in a list
    partial_results = ["", "", "", ""]

    # Helper function: runs the pipeline for a single track
    async def run_track(track_index: int):
        """
        Steps for each track:
          1) pick prompt A or B
          2) pick LLM A or B
          3) generate
          4) refine
          5) sanitize
          6) return final text
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

        # 2) Refine distractors
        refine_msg = await template_refine.aformat_prompt(write_fluster_result=write_fluster_result)
        refine_resp = await llm_refine.ainvoke(refine_msg.to_messages())
        refined_output = getattr(refine_resp, "content", refine_resp)

        # 3) Sanitize
        sanitize_msg = await template_sanitize.aformat_prompt(refinement_result=refined_output)
        sanitize_resp = await llm_sanitize.ainvoke(sanitize_msg.to_messages())
        sanitized_output = getattr(sanitize_resp, "content", sanitize_resp)

        return track_index, sanitized_output

    # Prepare the 4 tasks
    tasks = [
        run_track(0),
        run_track(1),
        run_track(2),
        run_track(3),
    ]

    # Run them in parallel
    for coro in asyncio.as_completed(tasks):
        track_idx, final_text = await coro
        partial_results[track_idx] = final_text

        # Yield partial update (4-tuple). The UI will map each item to a separate textbox.
        yield tuple(partial_results)
