# chains/diagnoser_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate
from config.exercise_standardizer import standardize_exercise


class DiagnoserChain(BaseModel):
    template_standardize: ChatPromptTemplate
    llm_standardize: Any  # Fixed LLM for step 1
    template_diagnose: ChatPromptTemplate
    llm_diagnose: Any  # User-selectable LLM for step 2

    async def run(self, user_query: str, exercise_format: str) -> str:
        """
        Runs the composite chain:
          1. Standardizes the exercise formatting (if exercise_format isn't Raw).
          2. Generates a diagnosis from the standardized format.
        """
        # --- Step 1: Standardize the exercise formatting (if exercise_format isn't 'Raw (original)') ---
        standardized_exercise = await standardize_exercise(
            user_query, exercise_format, self.template_standardize, self.llm_standardize
        )

        # --- Step 2: Generate a diagnosis using the standardized exercise ---
        prompt_diagnose = await self.template_diagnose.aformat_prompt(standardized_exercise=standardized_exercise)
        diagnose_messages = prompt_diagnose.to_messages()
        diagnosis = await self.llm_diagnose.ainvoke(diagnose_messages)

        return diagnosis.content if hasattr(diagnosis, "content") else diagnosis

    class Config:
        arbitrary_types_allowed = True
