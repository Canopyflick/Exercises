# chains/diagnoser_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class DiagnoserChain(BaseModel):
    template_standardize: ChatPromptTemplate
    template_diagnose: ChatPromptTemplate
    llm_standardize: Any  # Fixed LLM for step 1
    llm_diagnose: Any  # User-selectable LLM for step 2

    async def run(self, user_query: str, exercise_format: str) -> str:
        """
        Runs the composite chain:
          1. Standardizes the exercise description (if exercise_format isn't Raw).
          2. Generates a diagnosis from the standardized format.
        """
        # --- Step 1: Standardize the exercise description ---
        if exercise_format == "Raw (original)":
            standardized_exercise = user_query
        else:
            mapping = {
                "Markdown": "Please format the exercise in Markdown.",
                "XML": "Please format the exercise in XML.",
                "Plaintext": "Please format the exercise in plain text."
            }
            formatting_instructions = mapping.get(exercise_format, "Please format the exercise in Markdown.")
            prompt_std = await self.template_standardize.aformat_prompt(
                user_input=user_query,
                formatting_instructions=formatting_instructions
            )
            std_messages = prompt_std.to_messages()
            standardized_exercise = await self.llm_standardize.ainvoke(std_messages)

        # --- Step 2: Generate a diagnosis using the standardized exercise ---
        prompt_diag = await self.template_diagnose.aformat_prompt(standardized_exercise=standardized_exercise)
        diag_messages = prompt_diag.to_messages()
        diagnosis = await self.llm_diagnose.ainvoke(diag_messages)
        return diagnosis

    class Config:
        arbitrary_types_allowed = True
