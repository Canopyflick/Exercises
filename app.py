# app.py
import gradio as gr
import os
import asyncio
import logging

from utils.auth import login as auth_login  # simple login function
from config.chain_configs import chain_configs  # chain configurations dictionary

logger = logging.getLogger(__name__)


async def run_chain(chain_name: str, input_variables: dict):
    """
    A generic async function to run a given structured chain.
    Handles prompt formatting, invoking the LLM asynchronously, and returning results.

    Args:
        chain_name (str): The key for the desired chain in the chain_configs.
        input_variables (dict): A dictionary of variables to format the chain's prompt.

    Returns:
        The result of invoking the chain's LLM with the formatted prompt.
    """
    try:
        # Resolve the chain configuration by its name.
        chain_config = chain_configs.get(chain_name)
        if not chain_config:
            raise KeyError(f"Chain '{chain_name}' not found in the chain configuration.")

        # Generate the prompt using the chain's template.
        prompt_value = chain_config["template"].format_prompt(**input_variables)

        # Invoke the chain's LLM asynchronously.
        result = await chain_config["chain"].ainvoke(prompt_value.to_messages())

        logger.info(f"Chain '{chain_name}' executed successfully.")
        return result

    except KeyError as e:
        logger.error(f"Chain configuration error: {e}")
        raise ValueError(f"Invalid chain structure: missing {e}")

    except Exception as e:
        logger.error(f"Error running chain '{chain_name}': {e}")
        raise RuntimeError(f"Failed to execute chain: {e}")


async def run_diagnoser(user_query: str) -> str:
    """
    Async function to run the diagnoser chain.
    Prepares the input variables and awaits the chain's result.
    """
    input_vars = {"user_query": user_query}
    result = await run_chain("diagnoser", input_vars)
    return result


async def run_distractors(user_query: str) -> str:
    """
    Async function to run the distractors brainstorm chain.
    Prepares the input variables and awaits the chain's result.
    """
    input_vars = {"user_query": user_query}
    result = await run_chain("distractors", input_vars)
    return result


# -------------------------------
# Build the Gradio Interface
# -------------------------------
with gr.Blocks() as demo:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(
            label="Enter Password",
            type="password",
            placeholder="Enter password to access the app"
        )
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")  # For error messages

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:
        gr.Markdown("## Core Functionalities")
        with gr.Tabs():
            with gr.TabItem("Diagnoser"):
                gr.Markdown("### Diagnoser")
                diagnoser_input = gr.Textbox(
                    label="Enter Diagnoser Query",
                    placeholder="Type your query here..."
                )
                diagnoser_button = gr.Button("Submit")
                diagnoser_output = gr.Textbox(label="Response", interactive=False)
            with gr.TabItem("Distractors brainstorm"):
                gr.Markdown("### Distractors brainstorm")
                distractors_input = gr.Textbox(
                    label="Enter Brainstorm Query",
                    placeholder="Type your query here..."
                )
                distractors_button = gr.Button("Submit")
                distractors_output = gr.Textbox(label="Response", interactive=False)

    # -------------------------------
    # Set Up Interactions
    # -------------------------------

    # Login button: if the password is correct, hide the login container and reveal the main app.
    login_button.click(
        fn=auth_login,
        inputs=[password_input],
        outputs=[login_container, app_container, login_error]
    )

    # Run the Diagnoser chain asynchronously.
    diagnoser_button.click(
        fn=run_diagnoser,
        inputs=[diagnoser_input],
        outputs=[diagnoser_output]
    )

    # Run the Distractors brainstorm chain asynchronously.
    distractors_button.click(
        fn=run_distractors,
        inputs=[distractors_input],
        outputs=[distractors_output]
    )

# Launch the Gradio app.
demo.launch()
