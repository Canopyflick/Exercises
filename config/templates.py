from langchain_core.prompts import ChatPromptTemplate

dummy_template = ChatPromptTemplate([
    ("system", """
    SYSTEM MESSAGE 
    {bot_name} {weekday} {now}
    """),
    ("human", """
    USER MESSAGE 
    {user_message}
    """),
])

initial_classification_template = ChatPromptTemplate([
    ("system", """
    # Answer structure
    1. First pick the user_message_language: choose from Literal['English', 'German', 'Dutch', 'other']. 
       Look only at the user message. When multiple languages are present, pick the dominant one.
    2. Then, state your classification: 'Goals', 'Reminders', 'Meta', or 'Other'.
    """),
    ("human", """
    USER MESSAGE 
    {user_message}
    """),
])