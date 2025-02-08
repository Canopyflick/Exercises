# config/chain_configs.py
from config.templates import standardize_template, diagnose_template, distractors_template
from chains.diagnoser_chain import DiagnoserChain
from chains.distractors_chain import DistractorsChain
from config.llm_config import llms

# Note: The default LLM here is 4o; the UI can override this choice.
chain_configs = {
    "diagnoser": {
        "class": DiagnoserChain,
        "template_standardize": standardize_template,
        "template_diagnose": diagnose_template,
        "llm_standardize": llms["GPT-4o-mini"],  # Always fixed
        "llm_diagnose": llms["GPT-4o"],          # Default; can be replaced in UI
    },
    "distractors": {
        "class": DistractorsChain,
        "template": distractors_template,
        "llm": llms["GPT-4o"],
    },
}
