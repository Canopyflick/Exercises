# exercise_standardizer.py
from format_mappings import FORMAT_MAPPINGS
from langchain_core.prompts import ChatPromptTemplate
from typing import Any
from config.format_mappings import FORMAT_MAPPINGS

async def standardize_exercise(user_query: str, exercise_format: str, template: ChatPromptTemplate, llm: Any) -> str:
    """
    Standardizes an exercise's format using the specified template and LLM.
    Uses token streaming for efficiency.
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

    # Stream tokens to construct the standardized response
    standardized_exercise = ""
    async for token in llm.astream(std_messages):
        standardized_exercise += token

    return standardized_exercise
