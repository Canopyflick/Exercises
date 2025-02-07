from pydantic import BaseModel


class DistractorsChain(BaseModel):
    template: str
    llm: any

    def run(self, user_query: str) -> str:
        prompt = f"Brainstorm some distractors for:\n{user_query}"
        response = self.llm.call(prompt)
        return response
