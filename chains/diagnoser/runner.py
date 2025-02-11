# chains/diagnoser/diagnoser_runner.py
import asyncio

from config.chain_configs import chain_configs
from app.helpers.exercise_standardizer import standardize_exercise
from config.llm_config import llms


async def run_diagnoser(user_query: str, model_choice_diagnose: str, exercise_format_diagnose: str, sampling_count_diagnose: str) -> tuple:
    """
    Diagnose exercise(s) in parallel using a configured DiagnoserChain.

    This function:
      1. Standardizes the exercise text once using the chain's fixed LLM.
      2. Instantiates the DiagnoserChain with a user-selected diagnosing LLM.
      3. Performs multiple diagnoses in parallel (as many times as `sampling_count_validate`).
      4. Pads the results to ensure a fixed number of output fields (10).

    Args:
        user_query (str): Raw exercise data submitted by the user.
        model_choice_diagnose (str): The key/name of the chosen LLM for diagnosing.
        exercise_format_diagnose (str): The desired format for standardizing the exercise.
        sampling_count_diagnose (str): A string representing how many diagnoses to run concurrently (e.g., "3").

    Returns:
        tuple: A tuple of length 10, each containing a diagnosis result (or empty string if not enough samples).
    """
    # figure out how many times to run
    num_samples = int("".join(filter(str.isdigit, sampling_count_diagnose)))

    # Fetch the DiagnoserChain configuration.
    config = chain_configs["diagnoser"]

    # 1) Standardize the user query exactly once
    standardized_exercise = await standardize_exercise(
        user_query,
        exercise_format_diagnose,
        config["template_standardize"],  # Only if you kept them in config
        config["llm_standardize"]
    )

    # 2) Instantiate the DiagnoserChain using the user-selected LLM for diagnosing
    chain_instance = config["class"](
        templates_diagnose=config["templates_diagnose"],
        llm_diagnose=llms.get(model_choice_diagnose, config["llm_diagnose"]),
        template_diagnose_scorecard=config["template_diagnose_scorecard"],
        llm_4o_mini=config["llm_4o_mini"],
        llm_4o=config["llm_4o"]
    )

    # 3) Run the multiple samples in parallel
    # Create a short helper that does only the "diagnose" steps:
    tasks = [
        chain_instance.diagnose_only(standardized_exercise)
        for _ in range(num_samples)
    ]
    # run concurrently
    responses = await asyncio.gather(*tasks)

    # pad up to 10 if needed
    all_responses = list(responses) + [""] * (10 - len(responses))

    # Return a tuple of exactly 5 responses.
    return tuple(all_responses) + (standardized_exercise,)
