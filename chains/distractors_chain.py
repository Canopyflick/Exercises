# chains/distractors_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class DistractorsChain(BaseModel):
    template: ChatPromptTemplate
    llm: Any

    async def run(self, user_query: str) -> str:
        prompt = await self.template.aformat_prompt(user_input=user_query)
        messages = prompt.to_messages()
        result = await self.llm.ainvoke(messages)
        return result

    class Config:
        arbitrary_types_allowed = True
