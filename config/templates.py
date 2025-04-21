# config/templates.py
from langchain_core.prompts.chat import ChatPromptTemplate
# config/templates.py
from config.system_prompt_texts import (
    template_standardize_exercise_text,
    template_standardize_studytext_text,
    template_diagnose_double_negation_text,
    template_diagnose_correct_answer_stands_out_text,
    template_diagnose_distractor_clearly_wrong_text,
    template_diagnose_distractor_partially_correct_text,
    diagnose_scorecard_template_text,
    template_distractors_brainstorm_1_text,
    template_distractors_brainstorm_2_text,
    template_consolidate_distractors_text,
    template_gen_prompt_a_text,
    template_gen_prompt_b_text,
    template_sanitize_learning_objectives_text,
    template_write_fluster_a_text,
    template_write_fluster_b_text,
    template_refine_fluster_text,
    template_sanitize_fluster_text, template_isolate_exercises_text,
)


template_standardize_exercise = ChatPromptTemplate(
    messages=[
        ("system", "You reformat a given multiple choice exercise into a standardized format for future human processing. {formatting_instructions}\n\n"
                   "Only 3 elements are always mandatory:\n"
                   "1. A question or statement that starts with 'Vraag:' or 'Stelling:' (or their semantic equivalents in the language of the exercise).\n"
                   "2. A minimum of two answer options (in the spirit of 'multiple choice'), one of them the correct answer.\n"
                   "3. An indication of what the correct answer is.\n\n"
                   "Always return an exercise with at least these mandatory elements. If any of the 3 elements are missing "
                   "in the given exercise, do your educated best to make them up. Except for the 3 mandatory elements, never make up any "
                   "new content that was not present in the given exercise. For example, if the exercise doesn't include an explanation, completely leave this out in your version as well. You should sometimes leave out certain content "
                   "that is there, like any artifacts in the given exercise that don't contribute to its understandability."),
        ("human", "Here's the given exercise:\n{user_input}")
    ],
    input_variables=["user_input", "formatting_instructions"]
)

template_standardize_studytext = ChatPromptTemplate(
    messages=[
        ("system", "You reformat a given study text into a standardized format. {formatting_instructions}\n\n"
                   ),
        ("human", "Here's the given study text:\n{user_input}")
    ],
    input_variables=["user_input", "formatting_instructions"]
)

template_diagnose_double_negation = ChatPromptTemplate(
    messages=[
        ("system", template_diagnose_double_negation_text),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

template_diagnose_correct_answer_stands_out = ChatPromptTemplate(
    messages=[
        ("system", template_diagnose_correct_answer_stands_out_text),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

# <example where X>
# <exercise>
# </exercise>
# <explanation how the correct answer stands out>
# </explanation how the correct answer stands out>
# </example where X>

template_diagnose_distractor_clearly_wrong = ChatPromptTemplate(
    messages=[
        ("system", template_diagnose_distractor_clearly_wrong_text),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

template_diagnose_distractor_partially_correct = ChatPromptTemplate(
    messages=[
        ("system", template_diagnose_distractor_partially_correct_text),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

diagnose_scorecard_template = ChatPromptTemplate(
    messages=[
        ("system", """You analyze the results of the diagnoses of 4 potential issues that multiple choice exercises sometimes have, and consolidate those into a very simple one-line visual scorecard that summarizes all issues' diagnoses, to show the results clearly in one overview. The diagnoses concern the following 4 potential issues:
        1. Double negatives (if the exercise contains something like 'to not not do something', this is undesirable)
        2. The correct multiple choice answer option stands out from the rest (this is a hint for the student)
        3. A distractors answer option is too obviously false (it's useless, no student would ever pick it)
        4. A distractors answer option is too close to the truth (it's misleading, if a student picks it some experts might agree they are correct) 
        Use these two icons: 
        - ✅ means the diagnosis of the issue came back negative, so the issue is not present.
        - ❌ means the diagnosis of the issue came back positive, so the issue is present.
        (and a third icon if need be: - ❔ means the diagnosis is unclear)
        The scorecard should always look like this:
        <template>
        1. The exercise does not contain/contains a double negative: ✅/❌ -- 2. The correct answer does not/does stand out: ✅/❌ -- 3. None/Some of the distractors are too close to the truth: ✅/❌ -- 4. None/Some of the distractors are too close to the truth: ✅/❌
        </template>
        <example 1>
        1. The exercise doesn't contain a double negative: ✅ -- 2. The correct answer does not stand out: ✅ -- 3. None of the distractors are too obviously false: ✅ -- 4. None of the distractors are too close to the truth: ✅
        </example 1>
        <example 2>
        1. The exercise doesn't contain a double negative: ✅ -- 2. The correct answer does stand out: ❌ -- 3. None of the distractors are too obviously false: ✅ -- 4. Some of the distractors are too close to the truth: ❌
        </example 2>
        <example 3>
        1. The exercise contains a double negative: ❌ -- 2. The correct answer does not stand out: ✅ -- 3. Some of the distractors are too obviously false: ❌ -- 4. None of the distractors are too close to the truth: ✅
        </example 3>
        Oftentimes, diagnoses will be elaborate and quite nuanced, first viewing the issue from different angles, considering both scenarios of passing and failing equally. For this reason, when deciding on your binary classification, you should focus only on the very last concluding sentences of each diagnosis to determine an ultimate pass or fail.
        """),
        ("human", "For context, here is the exercise that's being diagnosed:\n"
                  "{standardized_exercise}\n\n"
                  "Here are the diagnoses:\n"
                  "{combined_diagnosis}")
    ],
    input_variables=["combined_diagnosis", "standardized_exercise"]
)



template_distractors_brainstorm_1 = ChatPromptTemplate(
    messages=[
        ("system", "Help me brainstorm. Based on the given multiple choice exercise, come up with{intermediate_distractors_specification}additional distractors: "
                   "alternative answer options that are not correct answers to the question, yet neither so implausible that even poorly informed students could immediately dismiss and eliminate them. (use the same language as the existing exercise)."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)

template_distractors_brainstorm_2 = ChatPromptTemplate(
    messages=[
        ("system", "Help me brainstorm answer options for a multiple choice exercise. Based on the given question, come up with{intermediate_distractors_specification}additional alternative distractors: "
                   "alternative answer options that are not correct, yet neither so implausible that even poorly informed students could immediately dismiss and eliminate them.\n\n"
                   "You can think about this as a spectrum between 'too correct' & 'too obviously false'. Or, in other words, a spectrum between two extreme ends that can be described as: "
                   "'An answer option that is not the correct answer to the question, yet extremely similar in meaning and scope to the correct answer, such that it's very debatable whether this answer option is not in fact also actually correct' & "
                   "'An answer option that is exceedingly unlikely, fantastical, off-base or ridiculous and therefore maximally obviously incorrect, such that no one who can read would think this could ever be the correct answer to the question'\n"
                   "Whether any particular distractors falls on the 'too correct' or 'too obviously incorrect' parts of the spectrum, is highly context-dependent. "
                   "This often depends on many aspects to do with question, for example its exact phrasing, specific (background) domain-knowledge related to the subject, "
                   "and assumptions about what test takers in the target group for this exercise already can be assumed to know or not know, and their intelligence.\n"
                   "In other words, it is not easy to pick distractors that are positioned inside the acceptable range on this spectrum. "
                   "Therefore, really try to go about your task here methodically: first establish the borders of the acceptable range of distractors by lingering there for a bit; taking into account the specific context of the given question, as follows.\n\n"
                   "Before drafting the final list, first come up with one or two faulty distractors, that are faulty in the sense that they would be júst too much on the 'too correct' side of the aforementioned spectrum.\n"
                   "Then, come up with one or two distractors that are júst faulty on the other side of that spectrum: júst too much on the side of 'too obviously false'.\n"
                   "As an intuition pump for the first category (distractors that are júst too correct), try to imagine experts in the question's domain discussing the answer option, and some of them arguing that the distractors would also be a valid answer to the given question. "
                   "As an intuition pump for the second category (distractors that are júst too obviously incorrect), try to image a student who is both generally stupid (bottom of his class) ánd uninformed about the given topic (didn't prepare for the test). Would even they júst so find it easy to eliminate the faulty distractors as clearly false?\n"
                   "Those are the two bounds of the spectrum range we aim to operate between during brainstorming.\n"
                   "So, through the above process of picking some júst faulty distractors in the context of the given question, both barely too correct and barely too obviously false, you establish the two bounds of acceptable distractors. When brainstorming, don't play it entirely safe though; when in doubt about where exactly on the spectrum the distractors would lie, just list the distractors you came up with anyway.\n\n"
                   "Next, in the brainstorming phase, it's most important that you get really creative and really try to think outside the box, to come up with the required potential alternative answer options to the exercise. We want to approach this task from all different angles, "
                   "to arrive at a varied selection of options, to serve as inspiration for a later stage of final selection (not now) to make the exercise the best it can be. For now, carry out the above-described prep in writing, then draft the list of{intermediate_distractors_specification}alternative distractors (in the same language as the existing exercise)."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)


template_consolidate_distractors  = ChatPromptTemplate(
    messages=[
        ("system", "You are given several lists of potential distractors (answer options to a multiple choice exercise), that need to be consolidated and/or trimmed down into one list. "
                   "Always at least filter out duplicates, do some logical sorting, and return one plain list{final_distractors_specification}. "
                   "Only focus on the distractors (answer options) themselves, don't carry over any reasoning about them. Return only the list. Format the list without numbering or bullet points, just put one distractors per line. Use the same language as the existing exercise.\n\n"
                   "For context, this is the exercise that the distractors are about:\n "
                   "{standardized_exercise}"),
        ("human", "Here are the lists:\n "
                  "{brainstorm_outputs}\n\n "
                  "--- end of lists ---\n\n"
                  "Now, your task is to return one plain list{final_distractors_specification}.")
    ],
    input_variables=["standardized_exercise", "brainstorm_outputs", "final_distractors_specification"]
)


template_gen_prompt_a = ChatPromptTemplate(
    messages=[
        ("system", template_gen_prompt_a_text),
        ("human", "{standardized_text}")
    ],
    input_variables=["standardized_text"]
)


template_gen_prompt_b = ChatPromptTemplate(
    messages=[
        ("system", template_gen_prompt_b_text),
        ("human", "{standardized_text}")
    ],
    input_variables=["standardized_text"]
)

template_sanitize_learning_objectives = ChatPromptTemplate(
    messages=[
        ("system", "You are given the result of a brainstorming session that lead to the generation of learning objectives. Your task is to "
                   "turn this result into a neat clean prose list of just the learning objectives, nothing else. Do not translate or otherwise edit the learning objectives, just relay them as a list without explicit formatting: merely every learning objective on its own line, without newline separation.\n\n"
                   "Here's an example of what good output could look like:\n"
                   "<example of a perfect list>\n"
                   "De student weet dat de neus een zintuig is.\n"
                   "De student weet dat de tong een zintuig is.\n"
                   "De student weet dat de huid een zintuig is.\n"
                   "</example of a perfect list>\n"),
        ("human", "Here is the brainstorming result:\n "
                  "{raw_output}")
    ],
    input_variables=["raw_output"]
)


template_write_fluster_a = ChatPromptTemplate(
    messages=[
        ("system", template_write_fluster_a_text),
        ("human", "Here's the learning objective:\n"
                  "{learning_objective}")
    ],
    input_variables=["learning_objective"]
)

template_write_fluster_b = ChatPromptTemplate(
    messages=[
        ("system", template_write_fluster_b_text),
        ("human", "Here's the learning objective:\n"
                  "{learning_objective}")
    ],
    input_variables=["learning_objective"]
)


template_refine_fluster = ChatPromptTemplate(
    messages=[
        ("system", template_refine_fluster_text),
        ("human", "Here's the source data:\n"
                  "{write_fluster_result}")
    ],
    input_variables=["write_fluster_result"]
)

template_sanitize_fluster = ChatPromptTemplate(
    messages=[
        ("system", template_sanitize_fluster_text),
        ("human", "{refinement_result}")
    ],
    input_variables=["refinement_result"]
)

template_isolate_exercises = ChatPromptTemplate(
    messages=[
        ("system", template_isolate_exercises_text),
        ("human", "{fluster}")
    ],
    input_variables=["fluster"]
)

template_fix_exercise = ChatPromptTemplate(
    messages=[
        (
            "system",
            "You are a helpful assistant that fixes issues in a single multiple choice exercise "
            "based on diagnosis notes. Return an improved exercise that has the same amount of answer options as the original, and the same correct answer. For example, if the correct answer is 'Deze stelling is niet correct', then this must remain the correct answer."
        ),
        (
            "user",
            "Original exercise:\n{exercise_text}\n\nDiagnosis:\n{diagnosis}\n\n" # this is the scorecard summary, ideally I guess this would be the complete diagnoses of all issues 
            "Rewrite the exercise so that all issues in the diagnosis are resolved. "
            "Use the same structure (prompt, choice_id_1..4, correct_answer_id, explanation)."
        ),
    ],
    input_variables=["exercise_text", "diagnosis"]
)