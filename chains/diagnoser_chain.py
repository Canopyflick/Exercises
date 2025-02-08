# chains/diagnoser_chain.py
import asyncio
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
          1. Standardizes the exercise formatting.
          2. Feeds the standardized exercise into multiple diagnosis prompts in parallel.
          3. Combines the outputs from all prompts.
        """
        # Step 1: Standardize the exercise.
        standardized_exercise = await standardize_exercise(
            user_query, exercise_format, self.template_standardize, self.llm_standardize
        )

        # Step 2: Define an async helper to run a single diagnosis prompt.
        async def run_single(template: ChatPromptTemplate, idx: int) -> str:
            prompt = await template.aformat_prompt(standardized_exercise=standardized_exercise)
            messages = prompt.to_messages()
            diagnosis_response = await self.llm_diagnose.ainvoke(messages)
            content = diagnosis_response.content if hasattr(diagnosis_response, "content") else diagnosis_response
            return f"**Diagnosis {idx}:**\n{content}"

        # Launch all diagnosis tasks concurrently.
        tasks = [
            run_single(template, idx)
            for idx, template in enumerate(self.templates_diagnose, start=1)
        ]
        diagnoses = await asyncio.gather(*tasks)

        # Step 3: Combine the outputs from each prompt.
        combined_diagnosis = "\n\n---\n\n".join(diagnoses)
        return combined_diagnosis

    class Config:
        arbitrary_types_allowed = True
