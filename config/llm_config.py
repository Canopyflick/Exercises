# config/llm_config.py
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from openai import api_key

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define temperature presets (adjust as needed)
ZERO = 0
LOW = 0.2
MID = 0.6
HIGH = 1

# Factory functions for each provider
def create_openai_llm(model_name: str, temperature: float):
    return ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name, temperature=temperature)

def create_openai_reasoning_llm(model_name: str, reasoning_effort: str = None):
    # If reasoning_effort is provided, pass it; otherwise, avoid sending the parameter.
    if reasoning_effort:
        return ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name, reasoning_effort=reasoning_effort)
    else:
        return ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name)

def create_anthropic_llm(model_name: str, temperature: float):
    return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name=model_name, temperature=temperature)

def create_anthropic_reasoning_llm(model_name: str, reasoning_effort: str = None):
    # If reasoning_effort is provided, pass it; otherwise, avoid sending the parameter.
    if reasoning_effort:
        return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name=model_name, reasoning_effort=reasoning_effort)
    else:
        return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name=model_name)

def create_deepseek_llm(model_name: str, temperature: float):
    return ChatDeepSeek(api_key=DEEPSEEK_API_KEY, model_name=model_name, temperature=temperature)

def create_google_reasoning_llm(model_name: str):
    return ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model=model_name)

# all of them in one dictionary
llms = {
    # OpenAI models with temperature
    "GPT-4o (zero temp)": create_openai_llm("gpt-4o", ZERO),
    "GPT-4o (low temp)": create_openai_llm("gpt-4o", LOW),
    "GPT-4o (mid temp)": create_openai_llm("gpt-4o", MID),
    "GPT-4o (high temp)": create_openai_llm("gpt-4o", HIGH),
    "GPT-4o-mini (zero temp)": create_openai_llm("gpt-4o-mini", ZERO),
    "GPT-4o-mini (low temp)": create_openai_llm("gpt-4o-mini", LOW),
    "GPT-4 Turbo (low temp)": create_openai_llm("gpt-4-turbo-2024-04-09", LOW),
    "GPT-4.5 (low temp)": create_openai_llm("gpt-4.5-preview-2025-02-27", LOW),
    "GPT-4.5 (mid temp)": create_openai_llm("gpt-4.5-preview-2025-02-27", MID),

    # OpenAI reasoning models (no temperature)
    "o1 (low reasoning_effort)": create_openai_reasoning_llm("o1", reasoning_effort="low"),
    "o1 (high reasoning_effort)": create_openai_reasoning_llm("o1", reasoning_effort="high"),
    "o3-mini (low reasoning_effort)": create_openai_reasoning_llm("o3-mini", reasoning_effort="low"),
    "o3-mini (medium reasoning_effort)": create_openai_reasoning_llm("o3-mini", reasoning_effort="medium"),
    "o3-mini (high reasoning_effort)": create_openai_reasoning_llm("o3-mini", reasoning_effort="high"),
    "o3 (high reasoning_effort)🚧": create_openai_reasoning_llm("o3", reasoning_effort="high"),

    # Anthropic models (Claude)
    "Claude 3.5 (zero temp)": create_anthropic_llm("claude-3-5-sonnet-latest", ZERO),
    "Claude 3.5 (low temp)": create_anthropic_llm("claude-3-5-sonnet-latest", LOW),
    "Claude 3.5 (mid temp)": create_anthropic_llm("claude-3-5-sonnet-latest", MID),
    "Claude 3.5 (high temp)": create_anthropic_llm("claude-3-5-sonnet-latest", HIGH),
    "Claude 3.5 Haiku (zero temp)": create_anthropic_llm("claude-3-5-haiku-latest", ZERO),
    "Claude 3.5 Haiku (low temp)": create_anthropic_llm("claude-3-5-haiku-latest", LOW),
    "Claude 3.7": create_anthropic_reasoning_llm("claude-3-7-sonnet-latest"),

    # DeepSeek
    "Deepseek R1 (zero temp)🚧": create_deepseek_llm("deepseek-reasoner", ZERO),
    "Deepseek R1 (low temp)🚧": create_deepseek_llm("deepseek-reasoner", LOW),
    "Deepseek R1 (mid temp)🚧": create_deepseek_llm("deepseek-reasoner", MID),
    "Deepseek R1 (high temp)🚧": create_deepseek_llm("deepseek-reasoner", HIGH),

    # Google models (Gemini)
    "Gemini 2.5 Pro Experimental (zero temp)🚧": create_google_reasoning_llm(model_name= "gemini-2.5-pro-exp-03-25"),
}

# specific for Diagnosis tab
llms_most_wanted = {
    # OpenAI models
    "GPT-4o (zero temp)": create_openai_llm("gpt-4o", ZERO),
    "GPT-4o (low temp)": create_openai_llm("gpt-4o", LOW),
    "GPT-4o (mid temp)": create_openai_llm("gpt-4o", MID),
    "GPT-4o (high temp)": create_openai_llm("gpt-4o", HIGH),
    "GPT-4o-mini (zero temp)": create_openai_llm("gpt-4o-mini", ZERO),
    "GPT-4o-mini (low temp)": create_openai_llm("gpt-4o-mini", LOW),
    "GPT-4 Turbo (low temp)": create_openai_llm("gpt-4-turbo-2024-04-09", LOW),

    # OpenAI reasoning models (no temperature)
    "o1": create_openai_reasoning_llm("o1-2024-12-17"),
    "o3-mini (low-reasoning effort version)": create_openai_reasoning_llm("o3-mini", reasoning_effort="low"),
    "o3-mini (medium-reasoning effort version)": create_openai_reasoning_llm("o3-mini", reasoning_effort="medium"),
    "o3-mini (high-reasoning effort version)": create_openai_reasoning_llm("o3-mini", reasoning_effort="high"),

    # Anthropic models
    "Claude 3.5 (zero temp)": create_anthropic_llm("claude-3-5-sonnet-latest", ZERO),
    "Claude 3.5 (low temp)": create_anthropic_llm("claude-3-5-sonnet-latest", LOW),
    "Claude 3.5 (mid temp)": create_anthropic_llm("claude-3-5-sonnet-latest", MID),
    "Claude 3.5 (high temp)": create_anthropic_llm("claude-3-5-sonnet-latest", HIGH),
    "Claude 3.5 Haiku (zero temp)": create_anthropic_llm("claude-3-5-haiku-latest", ZERO),
    "Claude 3.5 Haiku (low temp)": create_anthropic_llm("claude-3-5-haiku-latest", LOW),

    # DeepSeek
    "Deepseek R1 (zero temp)🚧": create_anthropic_llm("deepseek-reasoner", ZERO),
    "Deepseek R1 (low temp)🚧": create_anthropic_llm("deepseek-reasoner", LOW),
    "Deepseek R1 (mid temp)🚧": create_anthropic_llm("deepseek-reasoner", MID),
    "Deepseek R1 (high temp)🚧": create_anthropic_llm("deepseek-reasoner", HIGH),
}
