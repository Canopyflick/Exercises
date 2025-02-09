# chains/diagnoser_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any, List
from langchain_core.prompts.chat import ChatPromptTemplate
from config.exercise_standardizer import standardize_exercise


class DiagnoserChain(BaseModel):
    template_standardize: ChatPromptTemplate
    llm_standardize: Any  # Fixed LLM for step 1
    templates_diagnose: List[ChatPromptTemplate]
    llm_diagnose: Any  # User-selectable LLM for step 2
    template_diagnose_scorecard: ChatPromptTemplate

    async def run(self, user_query: str, exercise_format: str) -> str:
        """
        Runs the composite chain:
          1. Standardizes the exercise formatting
          2. Feeds the standardized exercise into multiple diagnosis prompts in parallel
          3. Combines the outputs from each prompt.
          4. Generates one-line scorecard of combined diagnoses

        """
        # Step 1: Standardize the exercise.
        standardized_exercise = await standardize_exercise(
            user_query, exercise_format, self.template_standardize, self.llm_standardize
        )

        # Step 2: Define an async helper to run a single diagnosis prompt.
        async def run_single_diagnosis(template: ChatPromptTemplate, idx: int) -> str:
            prompt = await template.aformat_prompt(standardized_exercise=standardized_exercise)
            messages = prompt.to_messages()
            diagnosis_response = await self.llm_diagnose.ainvoke(messages)
            content = diagnosis_response.content if hasattr(diagnosis_response, "content") else diagnosis_response
            return f"[DIAGNOSIS {idx}]{content}"

        # Launch all diagnosis tasks concurrently.
        tasks = [
            run_single_diagnosis(template, idx)
            for idx, template in enumerate(self.templates_diagnose, start=1)
        ]
        diagnoses = await asyncio.gather(*tasks)

        # Step 3: Combine the outputs from each prompt.
        combined_diagnosis = "\n\n---\n".join(diagnoses)

        # Step 4: Generate scorecard
        prompt = await self.template_diagnose_scorecard.aformat_prompt(combined_diagnosis=combined_diagnosis)
        scorecard_messages = prompt.to_messages()
        scorecard_response = await self.llm_diagnose.ainvoke(scorecard_messages)
        scorecard = scorecard_response.content if hasattr(scorecard_response, "content") else scorecard_response

        return scorecard + "\n" + combined_diagnosis

    class Config:
        arbitrary_types_allowed = True
