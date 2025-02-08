# chains/diagnoser_chain.py
from pydantic import BaseModel
from typing import Any
from langchain_core.prompts.chat import ChatPromptTemplate

class DiagnoserChain(BaseModel):
    template_standardize: ChatPromptTemplate
    template_diagnose: ChatPromptTemplate
    llm_standardize: Any  # Fixed LLM for step 1
    llm_diagnose: Any  # User-selectable LLM for step 2

    async def run(self, user_query: str, exercise_format: str) -> str:
        """
        Runs the composite chain:
          1. Standardizes the exercise formatting (if exercise_format isn't Raw).
          2. Generates a diagnosis from the standardized format.
        """
        # --- Step 1: Standardize the exercise formatting ---
        if exercise_format == "Raw (original)":
            standardized_exercise = user_query
        else:
            mapping = {
                "Markdown": (
                    "Please format the exercise in Markdown, similarly to this example:\n\n"
                    "**Theorie**  \n"
                    "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
                    "---\n\n"
                    "**Vraag**  \n"
                    "Wat is de meest passende definitie van eenzaamheid?\n\n"
                    "1. Het gevoel geen connectie te hebben met anderen  \n"
                    "2. Regelmatig in je eentje zijn  \n"
                    "3. Beide bovenstaande  \n"
                    "4. Geen van bovenstaande  \n\n"
                    "**Correct antwoord:**  \n"
                    "1. Het gevoel geen connectie te hebben met anderen."
                ),
                "XML": (
                    "Please reformat in XML, following this example:\n"
                    "<exercise>\n"
                    "    <content>\n"
                    "        <question>Theorie:\n"
                    "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
                    "Vraag:\n"
                    "Wat is de meest passende definitie van eenzaamheid?</question>\n"
                    "        <choices>\n"
                    "            <choice id=\"1\">Het gevoel geen connectie te hebben met anderen</choice>\n"
                    "            <choice id=\"2\">Regelmatig in je eentje zijn</choice>\n"
                    "            <choice id=\"3\">Beide bovenstaande</choice>\n"
                    "            <choice id=\"4\">Geen van bovenstaande</choice>\n"
                    "        </choices>\n"
                    "    </content>\n"
                    "    <answer>\n"
                    "        <correct-choice>1</correct-choice>\n"
                    "        <explanation></explanation>\n"
                    "    </answer>\n"
                    "</exercise>"
                ),
                "Plaintext": (
                    "Please reformat in plain text, following this example:\n\n"
                    "Theorie\n"
                    "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
                    "Vraag\n"
                    "Wat is de meest passende definitie van eenzaamheid?\n\n"
                    "1. Het gevoel geen connectie te hebben met anderen\n"
                    "2. Regelmatig in je eentje zijn\n"
                    "3. Beide bovenstaande\n"
                    "4. Geen van bovenstaande\n\n"
                    "Correct antwoord:\n"
                    "1. Het gevoel geen connectie te hebben met anderen."
                )
            }
            formatting_instructions = mapping.get(exercise_format, "Please reformat the given exercise to ease further processing.")
            prompt_std = await self.template_standardize.aformat_prompt(
                user_input=user_query,
                formatting_instructions=formatting_instructions
            )
            std_messages = prompt_std.to_messages()
            standardized_exercise = await self.llm_standardize.ainvoke(std_messages)

        # --- Step 2: Generate a diagnosis using the standardized exercise ---
        prompt_diag = await self.template_diagnose.aformat_prompt(standardized_exercise=standardized_exercise)
        diag_messages = prompt_diag.to_messages()
        diagnosis = await self.llm_diagnose.ainvoke(diag_messages)
        return diagnosis

    class Config:
        arbitrary_types_allowed = True
