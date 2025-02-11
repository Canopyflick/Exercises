import asyncio
from typing import AsyncGenerator
from config.llm_config import llms
from config.chain_configs import chain_configs
from app.helpers.study_text_standardizer import standardize_studytext

async def run_learning_objectives_generator(
    user_input_text: str,
    model_choice_1: str,
    model_choice_2: str,
    text_format: str
) -> AsyncGenerator:
    """
    Orchestrates the entire pipeline:
      1) Standardize the study text
      2) Generate (2 prompts × 2 LLMs) => 4 partial results
      3) Sanitize each partial result
      4) Yield partial updates in real time as each track completes
    """
    # 1) Standardize the text once
    config = chain_configs["learning_objectives"]  # you define this in chain_configs.py
    standardized = await standardize_studytext(
        user_input_text, text_format,
        config["template_standardize"],
        config["llm_standardize"]
    )

    # Prepare references for the generation prompts:
    prompt_a = config["template_gen_prompt_a"]
    prompt_b = config["template_gen_prompt_b"]
    sanitize_prompt = config["template_sanitize"]

    # pick the LLMs from user choices (with fallback to config)
    llm_a = llms.get(model_choice_1, config["default_llm_a"])
    llm_b = llms.get(model_choice_2, config["default_llm_b"])

    llm_sanitize=llms.get(config["llm_sanitize"])

    # We will store the final sanitized results in an array of 4 strings
    # (2 prompts × 2 LLMs)
    partial_results = ["", "", "", ""]

    # We'll define a short async helper for each track:
    # 'track_index' is 0..3 so we know which of the 4 textboxes to fill
    # 'gen_prompt' is either prompt_a or prompt_b
    # 'gen_llm' is either llm_a or llm_b
    async def run_track(track_index: int, gen_prompt, gen_llm):
        # Step: generate
        gen_msg = await gen_prompt.aformat_prompt(standardized_text=standardized)
        gen_resp = await gen_llm.ainvoke(gen_msg.to_messages())
        generation_output = getattr(gen_resp, "content", gen_resp)

        # Step: sanitize
        sanitize_msg = await sanitize_prompt.aformat_prompt(raw_output=generation_output)
        sanitize_resp = await llm_sanitize.ainvoke(sanitize_msg.to_messages())  # or use a separate LLM for sanitization
        sanitized_output = getattr(sanitize_resp, "content", sanitize_resp)

        return (track_index, sanitized_output)

    # Build the 4 tasks:
    #  - track 0 => prompt A, LLM 1
    #  - track 1 => prompt B, LLM 1
    #  - track 2 => prompt A, LLM 2
    #  - track 3 => prompt B, LLM 2

    tasks = [
        run_track(0, prompt_a, llm_a),
        run_track(1, prompt_b, llm_a),
        run_track(2, prompt_a, llm_b),
        run_track(3, prompt_b, llm_b),
    ]

    # We'll run them in parallel and yield updates as each finishes
    done_count = 0
    for coro in asyncio.as_completed(tasks):
        track_index, final_text = await coro
        partial_results[track_index] = final_text
        done_count += 1

        # yield partial update
        # We yield a tuple with the 4 track results.
        # The UI will map each item to the correct textbox.
        yield tuple(partial_results) + (standardized, )

