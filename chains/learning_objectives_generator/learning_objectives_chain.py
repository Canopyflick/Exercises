# app/chains/learning_objectives/learning_objectives_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class LearningObjectivesChain(BaseModel):
    """
    """
    template_standardize: ChatPromptTemplate
    llm_standardize: Any
    template_gen_prompt_a: ChatPromptTemplate
    template_gen_prompt_b: ChatPromptTemplate
    default_llm_a: Any
    default_llm_b: Any
    template_sanitize: ChatPromptTemplate
    llm_sanitize: Any

    class Config:
        arbitrary_types_allowed = True
