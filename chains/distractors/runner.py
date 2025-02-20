# chains/distractors/runner_without.py
import asyncio

from config.chain_configs import chain_configs
from app.helpers.exercise_standardizer import standardize_exercise
from config.llm_config import llms

async def run_distractors(
    user_query: str,
    model_choice_distractors_1: str,
    model_choice_distractors_2: str,
    model_choice_distractors_3: str,
    exercise_format_distractors: str,
    sampling_count_distractors: str,
    intermediate_distractors_specification: str,
    final_distractors_specification: str,
) -> tuple:
    """
    Generate distractors by running the DistractorsChain multiple times in parallel.

    1. Standardizes the exercise text once using a fixed LLM.
    2. Constructs a DistractorsChain, where the user can pick two LLMs
       (e.g. one low-temp, one mid-temp) for parallel brainstorming steps.
    3. Invokes the chain ``num_samples`` times in parallel (based on ``sampling_count_distractors``),
       each time producing one consolidated distractors output.
    4. Pads the results to fill 10 output fields.
    """
    # 0) Parse how many concurrent runs (samples) we want
    num_samples = int("".join(filter(str.isdigit, sampling_count_distractors)))
    # Fetch the DistractorsChain configuration.
    config = chain_configs["distractors"]

    # 1) Standardize the user query once for all tracks
    standardized_exercise = await standardize_exercise(
        user_query,
        exercise_format_distractors,
        config["template_standardize"],
        config["llm_standardize"]
    )

    # 2) Build the DistractorsChain instance
    chain_instance = config["class"](
        template_distractors_brainstorm_1=config["template_distractors_brainstorm_1"],
        template_distractors_brainstorm_2=config["template_distractors_brainstorm_2"],
        llm_brainstorm_1=llms.get(model_choice_distractors_1, config["llm_brainstorm_1"]),  # User-selected LLM 1
        llm_brainstorm_2=llms.get(model_choice_distractors_2, config["llm_brainstorm_2"]),  # User-selected LLM 2
        template_consolidate=config["template_consolidate"],
        llm_consolidate=llms.get(model_choice_distractors_3, config["llm_consolidate"]),    # User-selected LLM 3
    )

    # 3) Create N tasks in parallel (one full distractors generation pipeline per sample)
    tasks = [
        chain_instance.run(standardized_exercise, intermediate_distractors_specification, final_distractors_specification) for _ in range(num_samples)
    ]
    results = await asyncio.gather(*tasks)

    # 4) Pad up to 10 outputs to correspond to 10 response fields
    all_responses = list(results) + [""] * (10 - len(results))

    return tuple(all_responses) + (standardized_exercise,)
