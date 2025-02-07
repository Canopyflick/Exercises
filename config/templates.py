# config/templates.py
from langchain_core.prompts.chat import ChatPromptTemplate

# Template to standardize the exercise description.
standardize_template = ChatPromptTemplate(
    messages=[
        ("system", "You are an exercise standardizer. Convert the given exercise description into a standardized format. Use XML-tags for this format, like this: "),
        ("human", "{user_input}")
    ],
    input_variables=["user_input"]
)

# Template to generate a diagnosis from the standardized exercise.
diagnose_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a diagnostic assistant. Based on the standardized exercise description, provide a detailed diagnosis of potential issues and improvements."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

# Template for the distractors brainstorm (a single-step chain).
distractors_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a brainstorming assistant. Provide creative distractors and brainstorm ideas based on the user input."),
        ("human", "{user_input}")
    ],
    input_variables=["user_input"]
)
