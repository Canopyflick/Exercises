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
    template_gen_prompt_b,
    template_sanitize_learning_objectives,
    template_write_fluster_a,
    template_write_fluster_b,
    template_refine_fluster,
    template_sanitize_fluster, template_isolate_exercises, template_fix_exercise,
)
from chains.diagnoser.diagnoser_chain import DiagnoserChain
from chains.distractors.distractors_chain import DistractorsChain
from chains.learning_objectives_generator.learning_objectives_chain import LearningObjectivesChain
from chains.exercises.fluster_writing_chain import FlusterWritingChain
from config.llm_config import llms

# Note: The default LLM here is GPT-4o (low temp); the UI can override this choice.

# Model name constants - these match the keys in llm_config.llms
class ModelNames:
    GPT4_ZERO = "GPT-4o (zero temp)"
    GPT4_LOW = "GPT-4o (low temp)"
    GPT4_MID = "GPT-4o (mid temp)"
    GPT4_MINI_ZERO = "GPT-4o-mini (zero temp)"
    O1_HIGH_REASONING = "o1 (high reasoning_effort)"
    O3_MINI_HIGH_REASONING = "o3-mini (high reasoning_effort)"

chain_configs = {
    "diagnoser": {
        "class": DiagnoserChain,
        "template_standardize": template_standardize_exercise,
        "llm_standardize": llms[ModelNames.GPT4_MINI_ZERO],     # Always fixed
        "llm_4o_mini": llms[ModelNames.GPT4_LOW],
        "llm_4o": llms[ModelNames.GPT4_LOW],
        # 4 different diagnosis templates (to run in parallel:
        "templates_diagnose": [
            template_diagnose_double_negation,
            template_diagnose_correct_answer_stands_out,
            template_diagnose_distractor_clearly_wrong,
            template_diagnose_distractor_partially_correct,
        ],
        "template_diagnose_scorecard": diagnose_scorecard_template,
        "llm_diagnose": llms[ModelNames.GPT4_LOW],             # Default; can be replaced in UI
    },
    "distractors": {
        "class": DistractorsChain,
        "template_standardize": template_standardize_exercise,
        "llm_standardize": llms[ModelNames.GPT4_MINI_ZERO],     # Always fixed
        "template_distractors_brainstorm_1": template_distractors_brainstorm_1,
        "template_distractors_brainstorm_2": template_distractors_brainstorm_2,
        "llm_brainstorm_1": llms[ModelNames.GPT4_LOW],
        "llm_brainstorm_2": llms[ModelNames.GPT4_MID],
        "template_consolidate": template_consolidate_distractors,
        "llm_consolidate": llms[ModelNames.GPT4_LOW],
    },
    "learning_objectives": {
        "class": LearningObjectivesChain,
        "template_standardize": template_standardize_studytext,
        "llm_standardize": llms[ModelNames.GPT4_MINI_ZERO],     # Always fixed
        "template_gen_prompt_a": template_gen_prompt_a,
        "template_gen_prompt_b": template_gen_prompt_b,
        "default_llm_a": llms[ModelNames.O1_HIGH_REASONING],
        "default_llm_b": llms[ModelNames.O3_MINI_HIGH_REASONING],
        "template_sanitize": template_sanitize_learning_objectives,
        "llm_sanitize": ModelNames.GPT4_MINI_ZERO,
    },
    "fluster": {
        "class": FlusterWritingChain,
        "template_write_fluster_a": template_write_fluster_a,
        "template_write_fluster_b": template_write_fluster_b,
        "default_llm_a": llms[ModelNames.O1_HIGH_REASONING],
        "default_llm_b": llms[ModelNames.O3_MINI_HIGH_REASONING],
        # Prompt & LLM for the refine-distractors step
        "template_refine_fluster": template_refine_fluster,
        "llm_refine": llms[ModelNames.GPT4_ZERO],
        "template_sanitize": template_sanitize_fluster,
        "llm_sanitize": ModelNames.GPT4_MINI_ZERO,
        "template_structurize": template_isolate_exercises,
        "llm_structurize": llms[ModelNames.GPT4_ZERO],
        "template_fix_exercise": template_fix_exercise,
        "llm_fix_exercise": llms[ModelNames.GPT4_LOW],
    },
}
