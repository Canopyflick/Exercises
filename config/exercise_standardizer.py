# exercise_standardizer.py
import gradio as gr
from langchain_core.prompts import ChatPromptTemplate
from typing import Any
from config.format_mappings import FORMAT_MAPPINGS
from utils.state_manager import standardized_format_state


async def standardize_exercise(user_query: str, exercise_format: str, template: ChatPromptTemplate, llm: Any) -> str:
    """
    Standardizes an exercise's format using the specified template and LLM, and updates the UI via standardized_format_state.
    """
    if exercise_format == "Raw (original)":
        return user_query  # No transformation needed

    formatting_instructions = FORMAT_MAPPINGS.get(
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

    standardized_format_state.value = standardized_exercise

    return standardized_exercise

