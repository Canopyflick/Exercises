# config/chain_configs.py
from config.templates import (
    template_standardize_exercise,
    template_standardize_studytext,
    template_diagnose_double_negation,
    template_diagnose_correct_answer_stands_out,
    template_diagnose_distractor_clearly_wrong,
    template_diagnose_distractor_partially_correct,
    diagnose_scorecard_template,
    template_distractors_brainstorm_1,
    template_distractors_brainstorm_2,
    template_consolidate_distractors,
    template_gen_prompt_a,
    template_gen_prompt_b
)
from chains.diagnoser.diagnoser_chain import DiagnoserChain
from chains.distractors.distractors_chain import DistractorsChain
from chains.learning_objectives_generator.learning_objectives_chain import LearningObjectivesChain
from config.llm_config import llms

# Note: The default LLM here is GPT-4o (low temp); the UI can override this choice.

chain_configs = {
    "diagnoser": {
        "class": DiagnoserChain,
        "template_standardize": template_standardize_exercise,
        "llm_standardize": llms["GPT-4o-mini (zero temp)"],     # Always fixed
        "llm_4o_mini": llms["GPT-4o-mini (low temp)"],
        "llm_4o": llms["GPT-4o (low temp)"],
        # 4 different diagnosis templates (to run in parallel:
        "templates_diagnose": [
            template_diagnose_double_negation,
            template_diagnose_correct_answer_stands_out,
            template_diagnose_distractor_clearly_wrong,
            template_diagnose_distractor_partially_correct,
        ],
        "template_diagnose_scorecard": diagnose_scorecard_template,
        "llm_diagnose": llms["GPT-4o (low temp)"],             # Default; can be replaced in UI
    },
    "distractors": {
        "class": DistractorsChain,
        "template_standardize": template_standardize_exercise,
        "llm_standardize": llms["GPT-4o-mini (zero temp)"],     # Always fixed
        "template_distractors_brainstorm_1": template_distractors_brainstorm_1,
        "template_distractors_brainstorm_2": template_distractors_brainstorm_2,
        "llm_brainstorm_1": llms["GPT-4o (low temp)"],
        "llm_brainstorm_2": llms["GPT-4o (mid temp)"],
        "template_consolidate": template_consolidate_distractors,
        "llm_consolidate": llms["GPT-4o (low temp)"],  # or something else
    },
    "learning_objectives": {
        "class": LearningObjectivesChain,
        "template_standardize": template_standardize_studytext,
        "llm_standardize": llms["GPT-4o-mini (zero temp)"],     # Always fixed
        "template_gen_prompt_a": template_gen_prompt_a,
        "template_gen_prompt_b": template_gen_prompt_b,
        "default_llm_a": llms["o1"],
        "default_llm_b": llms["o3-mini (high reasoning_effort)"],
        "template_sanitize": template_sanitize_learning_objectives,
        "llm_sanitize": llms["GPT-4o-mini (zero temp)"],


    },
}

