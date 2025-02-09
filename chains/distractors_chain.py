# chains/distractors_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate
from config.exercise_standardizer import standardize_exercise


class DistractorsChain(BaseModel):
    template_distractors_brainstorm_1: ChatPromptTemplate
    template_distractors_brainstorm_2: ChatPromptTemplate
    llm_brainstorm_low: Any                  # User-selectable LLMs for brainstorm
    llm_brainstorm_high: Any
    template_consolidate: ChatPromptTemplate
    llm_consolidate: Any

    async def run(self, standardized_exercise: str) -> str:
        """
        Overall flow:
        2) Run 4 parallel brainstorming calls:
           - 2 uses 'template_distractors_brainstorm_1' with (low-temp, high-temp)
           - 2 uses 'template_distractors_brainstorm_2' with (low-temp, high-temp)
        3) Merge those four partial results in a single final answer
           via a "consolidation" prompt.
        4) Return the final string
        """

        # --- Step 2: Brainstorm in parallel ---
        async def run_brainstorm(
            prompt_template: ChatPromptTemplate,
            llm_brainstorm: Any,
            index_label: str
        ) -> str:
            # Format prompt
            prompt = await prompt_template.aformat_prompt(
                standardized_exercise=standardized_exercise
            )
            messages = prompt.to_messages()

            # Call the specified LLM
            response = await llm_brainstorm.ainvoke(messages)
            content = getattr(response, "content", response)

            return f"[Brainstorm {index_label}]\n{content}"

        tasks = []
        # Template 1, low-temp
        tasks.append(run_brainstorm(
            self.template_distractors_brainstorm_1,
            self.llm_brainstorm_1,
            "T1-Low"
        ))
        # Template 1, high-temp
        tasks.append(run_brainstorm(
            self.template_distractors_brainstorm_1,
            self.llm_brainstorm_2,
            "T1-High"
        ))
        # Template 2, low-temp
        tasks.append(run_brainstorm(
            self.template_distractors_brainstorm_2,
            self.llm_brainstorm_1,
            "T2-Low"
        ))
        # Template 2, high-temp
        tasks.append(run_brainstorm(
            self.template_distractors_brainstorm_2,
            self.llm_brainstorm_2,
            "T2-High"
        ))

        # Kick them off concurrently
        brainstorm_results = await asyncio.gather(*tasks)

        # Combine them in a single multiline string
        combined_brainstorms = "\n\n".join(brainstorm_results)

        # --- Step 3: Consolidate the 4 partial outputs into a final response ---
        consolidation_prompt = await self.template_consolidate.aformat_prompt(
            brainstorm_outputs=combined_brainstorms,
            standardized_exercise=standardized_exercise
        )
        consolidation_messages = consolidation_prompt.to_messages()

        consolidation_response = await self.llm_consolidate.ainvoke(consolidation_messages)
        final_output = getattr(consolidation_response, "content", consolidation_response)

        # Return the final merged distractors response
        return final_output

    class Config:
        arbitrary_types_allowed = True
