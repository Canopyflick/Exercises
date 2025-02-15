# chains/exercise_writing/fluster_writing_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class FlusterWritingChain(BaseModel):
    """
    A chain that:
      - Generates exercises from two prompts (A/B)
      - Refines distractors
      - Sanitizes final text
    """
    template_write_a: ChatPromptTemplate
    template_write_b: ChatPromptTemplate
    default_llm_a: Any
    default_llm_b: Any

    template_refine_distractors: ChatPromptTemplate
    llm_refine: Any

    template_sanitize_fluster: ChatPromptTemplate
    llm_sanitize: Any

    class Config:
        arbitrary_types_allowed = True
