from config.llm_config import llms
from config.templates import dummy_template, initial_classification_template
from chains.diagnoser_chain import DiagnoserChain
from chains.distractors_chain import DistractorsChain

chain_configs = {
    "diagnoser": {
        "template": dummy_template,
        "class": DiagnoserChain,
        "llm": llms["mini"],
    },
    "distractors": {
        "template": dummy_template,  # Replace with a specific template if needed.
        "class": DistractorsChain,
        "llm": llms["mini"],
    },
    # More chains can be added here.
}