# chains/diagnoser_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any, List
from langchain_core.prompts.chat import ChatPromptTemplate
from config.exercise_standardizer import standardize_exercise


class DiagnoserChain(BaseModel):
    templates_diagnose: List[ChatPromptTemplate]
    template_diagnose_scorecard: ChatPromptTemplate
    llm_diagnose: Any
    llm_4o_mini: Any

    async def diagnose_only(self, standardized_exercise: str) -> str:
        """
        Takes a PRE-standardized exercise and:
          (1) Runs multiple diagnosis prompts in parallel,
          (2) Merges the results,
          (3) Generates a scorecard line,
          (4) Returns the combined text + scorecard.
        """

        # Step 1: define an async helper to run each diagnosis in parallel
        async def run_single_diagnosis(template: ChatPromptTemplate, idx: int) -> str:
            prompt = await template.aformat_prompt(standardized_exercise=standardized_exercise)
            messages = prompt.to_messages()
            diagnosis_response = await self.llm_diagnose.ainvoke(messages)
            content = getattr(diagnosis_response, "content", diagnosis_response)
            return f"--- [DIAGNOSIS {idx}] ---\n{content}"

        # Step 2: launch all diagnoses concurrently
        tasks = [
            run_single_diagnosis(template, idx)
            for idx, template in enumerate(self.templates_diagnose, start=1)
        ]
        diagnoses = await asyncio.gather(*tasks)

        # Step 3: combine the outputs
        combined_diagnosis = "\n".join(diagnoses)

        # Step 4: Generate a one-line scorecard
        prompt = await self.template_diagnose_scorecard.aformat_prompt(
            combined_diagnosis=combined_diagnosis
        )
        scorecard_messages = prompt.to_messages()
        scorecard_response = await self.llm_4o.ainvoke(scorecard_messages)
        scorecard = getattr(scorecard_response, "content", scorecard_response)

        return combined_diagnosis + "\n\n" + scorecard

    class Config:
        arbitrary_types_allowed = True
