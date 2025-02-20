# app/helpers/exercise_standardizer.py
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Literal, List, Union

from pydantic import BaseModel

from config.format_mappings import FORMAT_MAPPINGS_EXERCISES



async def standardize_exercise(user_query: str, exercise_format: str, template: ChatPromptTemplate, llm: Any) -> str:
    """
    Standardizes an exercise's format using the specified template and LLM, and updates the UI via standardized_format_state.
    """
    if exercise_format == "Raw (original)":
        return user_query  # No transformation needed

    formatting_instructions = FORMAT_MAPPINGS_EXERCISES.get(
        exercise_format,
        "Please reformat the given exercise to ease further processing."
    )

    prompt_std = await template.aformat_prompt(
        user_input=user_query,
        formatting_instructions=formatting_instructions
    )

    std_messages = prompt_std.to_messages()
    response = await llm.ainvoke(std_messages)
    standardized_exercise = getattr(response, "content", response)

    return standardized_exercise


class Exercise(BaseModel):
    id: int
    prompt: str
    choice_id_1: str
    choice_id_2: str
    choice_id_3: Union[str, None]
    choice_id_4: Union[str, None]
    correct_answer_id: Literal[1, 2, 3, 4]
    explanation: Union[str, None]

class ExerciseSet(BaseModel):
    id: int
    exercises: List[Exercise]




async def structurize_exercise(
    fluster_text: str,
    template: ChatPromptTemplate,
    llm: Any   # e.g. ChatOpenAI
) -> ExerciseSet:
    """
    Distills individual exercises and their components from the fluster text
    using a structured-output call that returns a Fluster pydantic object.
    """
    # 1) Format the prompt
    prompt_str = await template.aformat_prompt(fluster=fluster_text)
    messages = prompt_str.to_messages()

    # 2) Call the LLM with the schema
    response = await llm.with_structured_output(ExerciseSet).ainvoke(messages)
    exercise_set = response.choices[0].message.parsed

    # If the model refused or the schema was violated, you might get None or an error
    if exercise_set is None:
        raise ValueError(f"LLM refusal or invalid structured data.\nLLM response: {response}")

    return exercise_set


def exercise_to_string(ex):
    choices = [ex.choice_id_1, ex.choice_id_2, ex.choice_id_3, ex.choice_id_4]
    choice_texts = [f"  {idx + 1}) {choice}" for idx, choice in enumerate(choices) if choice]

    correct_choice_text = next(
        (f"  Correct answer: {idx + 1}) {choice}"
         for idx, choice in enumerate(choices) if choice == ex.correct_answer_id),
        "  Correct answer: Unknown"
    )

    explanation_text = f"  Explanation: {ex.explanation}" if ex.explanation else ""

    plaintext_exercise = (
            f"Exercise {ex.id}:\n"
            f"  {ex.prompt}\n"
            + "\n".join(choice_texts) + "\n"
            + correct_choice_text + "\n"
            + explanation_text + "\n\n"
    )

    return plaintext_exercise

