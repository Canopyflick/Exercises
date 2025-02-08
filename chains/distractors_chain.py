# chains/distractors_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate
from config.exercise_standardizer import standardize_exercise


class DistractorsChain(BaseModel):
    template_standardize: ChatPromptTemplate
    template_distr: ChatPromptTemplate
    llm_standardize: Any            # Fixed LLM for step 1
    llm_distr: Any                  # User-selectable LLM for step 2


    async def run(self, user_query: str, exercise_format: str) -> str:
        """
        Runs the composite chain:
          1. Standardizes the exercise formatting (if exercise_format isn't Raw).
          2. Generates new distractors from the standardized format.
        """
        # --- Step 1: Standardize the exercise formatting (if exercise_format isn't 'Raw (original)') ---
        standardized_exercise = await standardize_exercise(
            user_query, exercise_format, self.template_standardize, self.llm_standardize
        )

        # --- Step 2: Generate new distractors using the standardized exercise ---
        prompt_distractors = await self.template_distractors.aformat_prompt(standardized_exercise=standardized_exercise)
        distractors_messages = prompt_distractors.to_messages()
        distractors = await self.llm_distr.astream(distractors_messages)

        return distractors

    class Config:
        arbitrary_types_allowed = True
