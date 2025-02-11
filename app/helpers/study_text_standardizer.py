# app/helpers/exercise_standardizer.py
from langchain_core.prompts import ChatPromptTemplate
from typing import Any
from config.format_mappings import FORMAT_MAPPINGS_STUDY_TEXTS



async def standardize_studytext(user_query: str, studytext_format: str, template: ChatPromptTemplate, llm: Any) -> str:
    """
    Standardizes a studytext's format using the specified template and LLM, and updates the UI via standardized_format_state.
    """
    if studytext_format == "Raw (original)":
        return user_query  # No transformation needed

    formatting_instructions = FORMAT_MAPPINGS_STUDY_TEXTS.get(
        studytext_format,
        "Please reformat the given studytext to ease further processing."
    )

    prompt_std = await template.aformat_prompt(
        user_input=user_query,
        formatting_instructions=formatting_instructions
    )

    std_messages = prompt_std.to_messages()
    response = await llm.ainvoke(std_messages)
    standardized_studytext = getattr(response, "content", response)

    return standardized_studytext

