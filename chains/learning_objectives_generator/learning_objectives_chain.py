# app/chains/learning_objectives/learning_objectives_chain.py
import asyncio
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class LearningObjectivesChain(BaseModel):
    """
    """

    class Config:
        arbitrary_types_allowed = True
