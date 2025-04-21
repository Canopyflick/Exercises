# chains/exercises/run_fluster_with_diagnosis.py
import asyncio
from typing import Tuple, List, Any

from app.helpers.exercise_standardizer import structurize_exercise, ExerciseSet, Exercise, exercise_to_string
from chains.exercises.runner_without import write_fluster_track
from config.chain_configs import chain_configs
from config.llm_config import llms

import json
from typing import List
from pydantic import ValidationError

from config.chain_configs import chain_configs
from app.helpers.exercise_standardizer import ExerciseSet, Exercise


async def parse_fluster_text_to_exercises(fluster_text: str) -> List[Exercise]:
    """
    Calls the fluster chain's template_structurize + llm_structurize
    with a structured output approach, expecting an ExerciseSet Pydantic object.
    Returns the list of Exercise objects.

    Raises ValueError if the LLM fails or refuses to parse,
    or if the LLM's output is invalid JSON for our schema.
    """

    # 1) Get the parse-related template & LLM from the fluster config
    config = chain_configs["fluster"]
    template_structurize = config["template_structurize"]
    llm_structurize = config["llm_structurize"]

    # 2) Format the prompt
    prompt_value = await template_structurize.aformat_prompt(fluster=fluster_text)
    messages = prompt_value.to_messages()

    # 3) Call the LLM with structured output
    #    If your version of langchain_openai supports .with_structured_output(ExerciseSet):
    exercise_set = await llm_structurize.with_structured_output(ExerciseSet).ainvoke(messages)

    if exercise_set is None:
        # If the LLM refused or the format was invalid, we might get None
        raise ValueError(
            f"LLM refused or returned invalid structured data.\nRaw content:\n{exercise_set}"
        )

    # 5) Return the exercises list
    #    If there's also an .id field at exercise_set.id, you can store it if needed.
    return exercise_set.exercises


async def _async_fluster_with_diagnosis(
    user_input_text: str,
    model_choice_1: str,
    model_choice_2: str
) -> Tuple[str, str, str, str, str, str, str, str]:
    """
    The core async pipeline:
      1. Generate fluster text for track0 & track2 (in parallel).
      2. Parse each text => get a list of Exercise objects.
      3. Diagnose each exercise => fix if needed.
      4. Build the final output strings for the UI.
    """
    fluster_config = chain_configs["fluster"]
    diagnoser_config = chain_configs["diagnoser"]

    llm1 = llms.get(model_choice_1, fluster_config["default_llm_a"])
    llm2 = llms.get(model_choice_2, fluster_config["default_llm_b"])

    # 1) Generate track0 & track2 in parallel
    track0_coro = write_fluster_track(
        user_input_text,
        model_choice_1,
        fluster_config,
        0
    )
    track2_coro = write_fluster_track(
        user_input_text,
        model_choice_2,
        fluster_config,
        2
    )

    (t0_idx, track0_text), (t2_idx, track2_text) = await asyncio.gather(track0_coro, track2_coro)

    # 2) Parse each final text => list of Exercises
    fluster0_exs = await parse_fluster_text_to_exercises(track0_text)
    fluster2_exs = await parse_fluster_text_to_exercises(track2_text)

    # 3) Diagnose + fix each exercise
    diag0_results, fixed0_exs = await diagnose_and_fix_all(fluster0_exs, diagnoser_config, llm_fix=llm1)
    diag2_results, fixed2_exs = await diagnose_and_fix_all(fluster2_exs, diagnoser_config, llm_fix=llm2)

    # 4) Convert the final exercises to strings for display
    # (Or you can store them back into a bigger data structure.)
    final0_text = build_fluster_text(fixed0_exs)
    final2_text = build_fluster_text(fixed2_exs)

    # We'll combine the diagnoses into single strings
    diagnosis_text_0 = "\n".join(diag0_results)
    diagnosis_text_2 = "\n".join(diag2_results)

    # 5) Return the 8 items in the order your UI needs
    #    (track0_text, "", track2_text, "", diag0_text, diag2_text, fixed0_text, fixed2_text)
    return (
        track0_text,   # box_0
        "",            # box_1 (unused)
        track2_text,   # box_2
        "",            # box_3 (unused)
        diagnosis_text_0,  # diagnosis_box_1
        diagnosis_text_2,  # diagnosis_box_3
        final0_text,       # fixes_box_1
        final2_text        # fixes_box_3
    )


async def write_fluster_track(
    user_input: str,
    model_choice_key: str,
    fluster_config: dict,
    track_index: int
) -> tuple[int, str]:
    """
    Uses the fluster chain config to write a single track's fluster.
    Returns (track_index, final_sanitized_text).
    """
    # 1) Decide prompt A or B
    if track_index in (0, 2):
        gen_template = fluster_config["template_write_fluster_a"]
    else:
        gen_template = fluster_config["template_write_fluster_b"]

    # 2) Decide LLM
    # either use model_choice_key from user, or the config's default
    fallback_llm = fluster_config["default_llm_a"] if track_index in (0, 1) else fluster_config["default_llm_b"]
    gen_llm = llms.get(model_choice_key, fallback_llm)

    # 3) Format + invoke the "writing" prompt
    prompt_value = await gen_template.aformat_prompt(learning_objective=user_input)
    gen_resp = await gen_llm.ainvoke(prompt_value.to_messages())
    raw_text = getattr(gen_resp, "content", gen_resp)

    # 4) (Optionally refine distractors) - if you have that step
    # ...
    # refine_msg = ...
    # refined_resp = await fluster_config["llm_refine"].ainvoke(...)
    # raw_text = refined_resp.content

    # 5) sanitize
    sanitize_template = fluster_config["template_sanitize"]
    llm_sanitize = fluster_config["llm_sanitize"]
    sanitize_prompt = await sanitize_template.aformat_prompt(refinement_result=raw_text)
    sanitize_resp = await llm_sanitize.ainvoke(sanitize_prompt.to_messages())
    final_text = getattr(sanitize_resp, "content", sanitize_resp)

    return (track_index, final_text)



async def diagnose_and_fix_all(
        exercises: List[Exercise],
        diagnoser_config: dict,
        llm_fix: Any) -> tuple[List[str], List[Exercise]]:
    """
    For each exercise, run the 'diagnose_only' from the DiagnoserChain,
    then interpret the results (scorecard) to see if we need a fix,
    then produce an updated exercise if needed.

    Returns:
      - a list of strings (one per exercise) summarizing the diagnosis,
      - a list of possibly fixed exercises.
      :param llm_fix:
    """
    diag_chain = diagnoser_config["class"](
        templates_diagnose=diagnoser_config["templates_diagnose"],
        template_diagnose_scorecard=diagnoser_config["template_diagnose_scorecard"],
        llm_diagnose=diagnoser_config["llm_diagnose"],
        llm_4o_mini=diagnoser_config["llm_4o_mini"],
        llm_4o=diagnoser_config["llm_4o"]
    )

    diag_strings = []
    fixed_exs = []

    # Could do parallel calls, but let's keep it simple here
    for ex in exercises:
        # 1) Build a standardized string from the exercise
        ex_str = exercise_to_string(ex)  # user-defined
        # 2) call diagnose_only => returns combined text + scorecard
        combined_diag, scorecard = await diag_chain.diagnose_only(
            ex_str
        )
        # 3) interpret the result
        diag_result = (
            f"Exercise {ex.id}:\n{combined_diag}\n--- [SCORECARD] ---\n{scorecard}"
        )
        diag_strings.append(diag_result)

        fluster_config = chain_configs["fluster"]

        if "❌" in scorecard:
            ex_fixed = await fix_exercise(ex, scorecard, fluster_config, llm_fix)
            fixed_exs.append(ex_fixed)
        else:
            fixed_exs.append(ex)

    return diag_strings, fixed_exs



async def diagnose_exercise(ex: Exercise) -> str:
    """
    Convert an Exercise object to a standardized string that DiagnoserChain can handle,
    then call DiagnoserChain.diagnose_only(...).
    """
    # 1) standardize or build a string from the exercise
    # e.g. "Vraag: ...\nA) ...\nB) ...\nCorrect=1"
    standardized_str = exercise_to_string(ex)

    # 2) get the chain config for "diagnoser"
    diag_config = chain_configs["diagnoser"]

    # 3) instantiate the chain object (if needed) or reuse a global one
    chain_instance = diag_config["class"](
        templates_diagnose=diag_config["templates_diagnose"],
        template_diagnose_scorecard=diag_config["template_diagnose_scorecard"],
        llm_diagnose=diag_config["llm_diagnose"],
        llm_4o_mini=diag_config["llm_4o_mini"],
        llm_4o=diag_config["llm_4o"]
    )

    # 4) call diagnose_only
    diagnosis = await chain_instance.diagnose_only(standardized_str)
    return diagnosis






from pydantic import ValidationError

async def fix_exercise(ex: Exercise, diag_str: str, cfg: dict, llm_fix:None) -> Exercise:
    tmpl_fix  = cfg["template_fix_exercise"]
    if not llm_fix:
        llm_fix   = cfg["llm_fix_exercise"]
    llm_cast  = cfg["llm_structurize"]          # already in chain_configs

    # 1️⃣ first call – creative rewrite
    prompt = await tmpl_fix.aformat_prompt(
                 exercise_text = exercise_to_string(ex),
                 diagnosis     = diag_str
             )
    raw = (await llm_fix.ainvoke(prompt.to_messages())).content

    # 2️⃣ second call – cast to schema
    try:
        ex_fixed = await llm_cast.with_structured_output(Exercise).ainvoke(
            [("user", raw)]                   # minimal prompt: just the text
        )
        return ex_fixed
    except Exception:
        return ex.copy(update={"prompt": raw})



def build_fluster_text(ex_list: list[Exercise]) -> str:
    """
    Combine the final fixed exercises into a user-facing block of text.
    """
    lines = []
    for ex in ex_list:
        lines.append(
            f"Exercise {ex.id}:\n"
            f"  {ex.prompt}\n"
            f"  1) {ex.choice_id_1}\n"
            f"  2) {ex.choice_id_2}\n"
            f"  3) {ex.choice_id_3}\n"
            f"  4) {ex.choice_id_4}\n"
            f"  Correct answer: {ex.correct_answer_id}\n"
            f"  Explanation: {ex.explanation}\n\n"
        )
    return "\n".join(lines)

async def run_fluster_with_diagnosis(
    user_input_text: str,
    model_choice_1: str,
    model_choice_2: str
) -> Tuple[str, str, str, str, str, str, str, str]:
    """
    Async entrypoint for the UI or external calls.
    """
    return await _async_fluster_with_diagnosis(user_input_text, model_choice_1, model_choice_2)