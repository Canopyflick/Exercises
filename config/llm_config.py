# config/llm_config.py
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_deepseek import ChatDeepSeek

# Retrieve API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Define temperature presets (adjust as needed)
ZERO = 0
LOW = 0.2
MID = 0.7
HIGH = 1.2

# Factory functions for each provider
def create_openai_llm(model_name: str, temperature: float):
    return ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name, temperature=temperature)

def create_openai_reasoning_llm(model_name: str):
    return ChatOpenAI(api_key=OPENAI_API_KEY, model_name=model_name)

def create_anthropic_llm(model_name: str, temperature: float):
    return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name=model_name, temperature=temperature)

def create_deepseek_llm(model_name: str, temperature: float):
    return ChatAnthropic(api_key=ANTHROPIC_API_KEY, model_name=model_name, temperature=temperature)

llms = {
    "GPT-4o": create_openai_llm("gpt-4o", LOW),
    "GPT-4o-mini": create_openai_llm("gpt-4o-mini", ZERO),
    "GPT-4o_high_temp": create_openai_llm("gpt-4o", HIGH),
    "GPT-4o-mini_high_temp": create_openai_llm("gpt-4o-mini", HIGH),
    "GPT-4 Turbo": create_openai_llm("gpt-4-turbo-2024-04-09", HIGH),
    "o1": create_openai_reasoning_llm("o1-2024-12-17"),
    "o3-mini": create_openai_reasoning_llm("o3-mini-2025-01-31"),
    "Claude 3.5": create_anthropic_llm("claude-3-5-sonnet-latest", LOW),
    "Deepseek R1🚧": create_anthropic_llm("deepseek-reasoner", LOW),
}