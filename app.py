# app.py
import gradio as gr
import os
import asyncio
import logging

from utils.auth import login as auth_login  # Simple authentication
from config.chain_configs import chain_configs
from config.llm_config import llms

logger = logging.getLogger(__name__)

# A generic async runner for chains.
async def run_chain(chain_name: str, input_variables: dict, selected_model: str):
    try:
        chain_config = chain_configs.get(chain_name)
        if not chain_config:
            raise KeyError(f"Chain '{chain_name}' not found.")

        # Override the LLM based on user selection.
        chosen_llm = llms.get(selected_model)
        if not chosen_llm:
            raise KeyError(f"LLM '{selected_model}' is not configured.")

        # Instantiate the chain with the chosen LLM.
        if chain_name == "diagnoser":
            chain_instance = chain_config["class"](
                template_standardize=chain_config["template_standardize"],
                template_diagnose=chain_config["template_diagnose"],
                llm=chosen_llm,
            )
        elif chain_name == "distractors":
            chain_instance = chain_config["class"](
                template=chain_config["template"],
                llm=chosen_llm,
            )
        else:
            raise KeyError(f"Chain '{chain_name}' is not implemented.")

        result = await chain_instance.run(input_variables["user_query"])
        logger.info(f"Chain '{chain_name}' executed successfully.")
        return result

    except Exception as e:
        logger.error(f"Error in run_chain for '{chain_name}': {e}")
        return f"Error: {e}"

# Async wrappers for each chain.
async def run_diagnoser(user_query: str, model_choice: str) -> str:
    return await run_chain("diagnoser", {"user_query": user_query}, model_choice)

async def run_distractors(user_query: str, model_choice: str) -> str:
    return await run_chain("distractors", {"user_query": user_query}, model_choice)

# -------------------------------
# Build the Gradio Interface
# -------------------------------
with gr.Blocks() as demo:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(label="Enter Password", type="password", placeholder="Enter password to access the app")
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:
        gr.Markdown("## Core Functionalities")
        # Dropdown for LLM selection.
        model_choice = gr.Dropdown(
            choices=list(llms.keys()),
            value="OpenAI",
            label="Select LLM Model",
            interactive=True,
        )
        with gr.Tabs():
            with gr.TabItem("Diagnoser"):
                gr.Markdown("### Diagnoser")
                diagnoser_input = gr.Textbox(label="Enter Diagnoser Query", placeholder="Type your exercise description here...")
                diagnoser_button = gr.Button("Submit")
                diagnoser_output = gr.Textbox(label="Diagnosis", interactive=False)
            with gr.TabItem("Distractors brainstorm"):
                gr.Markdown("### Distractors brainstorm")
                distractors_input = gr.Textbox(label="Enter Brainstorm Query", placeholder="Type your query here...")
                distractors_button = gr.Button("Submit")
                distractors_output = gr.Textbox(label="Response", interactive=False)

    # -------------------------------
    # Set Up Interactions
    # -------------------------------
    # Login button interaction.
    login_button.click(
        fn=auth_login,
        inputs=[password_input],
        outputs=[login_container, app_container, login_error]
    )

    # Note: Gradio supports async functions as callbacks.
    diagnoser_button.click(
        fn=run_diagnoser,
        inputs=[diagnoser_input, model_choice],
        outputs=[diagnoser_output]
    )
    distractors_button.click(
        fn=run_distractors,
        inputs=[distractors_input, model_choice],
        outputs=[distractors_output]
    )

# Launch the app.
demo.launch()
