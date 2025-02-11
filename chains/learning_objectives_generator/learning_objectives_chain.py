# app/chains/learning_objectives/learning_objectives_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class LearningObjectivesChain(BaseModel):
    """
    Orchestrates multi-step generation of learning objectives:
      1) Two parallel calls to 'learning_objective_generator' (LLM1, LLM2).
      2) Combine those outputs.
      3) 'learning_objective_eliminator' on the combined output (Main LLM).
      4) 'learning_objective_finetuner' on the output of that (Main LLM).
      5) 'learning_objective_presenter' to finalize (Main LLM).

    Each step can have its own ChatPromptTemplate and uses the relevant LLM.

    If you want a separate alt LLM for step #3 or #4, just expand as needed.
    """

    # Templates
    template_generator: ChatPromptTemplate
    template_eliminator: ChatPromptTemplate
    template_finetuner: ChatPromptTemplate
    template_presenter: ChatPromptTemplate

    # LLM references
    llm_main: Any   # The "Main LLM"
    llm_alt: Any    # The "Other LLM" used only for the second generator prompt

    async def run(self, standardized_studytext: str) -> str:
        """
        Main pipeline for a single run. The 'standardized_studytext' is assumed
        to be already standardized outside of this chain, so we jump straight to generation.
        """

        # 1) Two parallel calls to learning_objective_generator
        #    with different LLMs (llm_main vs. llm_alt).

        async def run_generator(llm, llm_label) -> str:
            # Format the generator prompt
            prompt = await self.template_generator.aformat_prompt(
                standardized_studytext=standardized_studytext,  # possibly other variables
                llm_label=llm_label
            )
            messages = prompt.to_messages()
            response = await llm.ainvoke(messages)
            return getattr(response, "content", response)

        # Launch in parallel
        gen_main_task = asyncio.create_task(run_generator(self.llm_main, "MAIN"))
        gen_alt_task  = asyncio.create_task(run_generator(self.llm_alt, "ALT"))

        # Wait for both to finish
        gen_main_result, gen_alt_result = await asyncio.gather(gen_main_task, gen_alt_task)

        # Combine them
        combined_generators = f"[GEN MAIN]\n{gen_main_result}\n\n[GEN ALT]\n{gen_alt_result}"

        # 2) learning_objective_eliminator (llm_main)
        prompt_eliminate = await self.template_eliminator.aformat_prompt(
            combined_generators=combined_generators,
            standardized_studytext=standardized_studytext
        )
        elim_messages = prompt_eliminate.to_messages()
        elim_response = await self.llm_main.ainvoke(elim_messages)
        elim_output = getattr(elim_response, "content", elim_response)

        # 3) learning_objective_finetuner (llm_main)
        prompt_fine = await self.template_finetuner.aformat_prompt(
            elimination_output=elim_output,
            standardized_studytext=standardized_studytext
        )
        fine_messages = prompt_fine.to_messages()
        fine_response = await self.llm_main.ainvoke(fine_messages)
        fine_output = getattr(fine_response, "content", fine_response)

        # 4) learning_objective_presenter (llm_main)
        prompt_present = await self.template_presenter.aformat_prompt(
            finetuned_output=fine_output,
            standardized_studytext=standardized_studytext
        )
        present_messages = prompt_present.to_messages()
        present_response = await self.llm_main.ainvoke(present_messages)
        final_output = getattr(present_response, "content", present_response)

        return final_output

    class Config:
        arbitrary_types_allowed = True
