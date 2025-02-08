# config/chain_configs.py
from config.templates import standardize_template, diagnose_template, distractors_template, \
    diagnose_double_negation_template, diagnose_correct_answer_stands_out_template, \
    diagnose_distractor_clearly_wrong_template, diagnose_distractor_partially_correct_template
from chains.diagnoser_chain import DiagnoserChain
from chains.distractors_chain import DistractorsChain
from config.llm_config import llms

# Note: The default LLM here is 4o; the UI can override this choice.
chain_configs = {
    "diagnoser": {
        "class": DiagnoserChain,
        "template_standardize": standardize_template,
        "llm_standardize": llms["GPT-4o-mini"],     # Always fixed
        # Provide a list of 4 different diagnosis templates:
        "templates_diagnose": [
            diagnose_double_negation_template,
            diagnose_correct_answer_stands_out_template,
            diagnose_distractor_clearly_wrong_template,
            diagnose_distractor_partially_correct_template,
        ],
        "llm_diagnose": llms["GPT-4o"],             # Default; can be replaced in UI
    },
    "distractors": {
        "class": DistractorsChain,
        "template_standardize": standardize_template,
        "llm_standardize": llms["GPT-4o-mini"],     # Always fixed
        "template_distractors": distractors_template,
        "llm_distractors": llms["GPT-4o"],                # Default; can be replaced in UI
    },
}
