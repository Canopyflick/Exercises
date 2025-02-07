from pydantic import BaseModel


class DiagnoserChain(BaseModel):
    template: str  # In practice, you might accept a ChatPromptTemplate
    llm: any  # Type the LLM appropriately (or use typing.Any for now)

    def run(self, user_query: str) -> str:
        # Here you would plug in your LangChain logic.
        # For demonstration, we mimic a call to an LLM:
        # In production, you could use an LLMChain or a sequence of chains.
        prompt = f"What is wrong with this exercise?\n{user_query}"
        response = self.llm.call(prompt)
        return response