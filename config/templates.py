# config/templates.py
from langchain_core.prompts.chat import ChatPromptTemplate

# Template to standardize the exercise description.
standardize_template = ChatPromptTemplate(
    messages=[
        ("system", "You reformat data on multiple choice exercises. Convert the given exercise(s) into a standardized format. {formatting_instructions}"),
        ("human", "{user_input}")
    ],
    input_variables=["user_input", "formatting_instructions"]
)

# Template to generate a diagnosis from the standardized exercise.
diagnose_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a diagnostic assistant. Based on the given exercise(s), provide a detailed diagnosis of potential issues. What makes this exercise sub-par, worse than it could be, not yet perfect? Only give the diagnosis, no solutions."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

# Template for the distractors brainstorm (a single-step chain).
distractors_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a brainstorming assistant. Based on the given multiple choice exercise, come up with 10 additional distractors: alternative answer options that are not correct, yet plausible enough that a poorly informed student might pick them. Vary the degree of 'almost correctness' and 'clearly incorrectness' between them to provide a wide range of options."),
        ("human", "{user_input}")
    ],
    input_variables=["standardized_exercise"]
)
