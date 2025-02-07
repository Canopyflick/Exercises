from langchain_openai import ChatOpenAI

ZERO = 0
LOW = 0.2
MID = 0.7
HIGH = 1.2

llms = {
    "gpt4o": ChatOpenAI(model_name="gpt-4o", temperature=LOW),
    "mini": ChatOpenAI(model_name="gpt-4o-mini", temperature=LOW),
    "gpt4o_high_temp": ChatOpenAI(model_name="gpt-4o", temperature=HIGH),
    "mini_high_temp": ChatOpenAI(model_name="gpt-4o-mini", temperature=HIGH),
    "o1": ChatOpenAI(model_name="o1"),
}