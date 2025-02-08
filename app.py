# app.py
import gradio as gr
import os
import asyncio
import logging

from utils.auth import login as auth_login  # Simple authentication
from config.chain_configs import chain_configs
from config.llm_config import llms

logger = logging.getLogger(__name__)

# --- Callback to update the exercise format dropdown based on LLM selection ---
def update_exercise_format(selected_model: str):
    # When "Claude3.5" is selected, default the format to XML; otherwise, default to Markdown.
    if selected_model == "Claude3.5":
        return gr.update(value="XML")
    else:
        return gr.update(value="Markdown")

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
async def run_diagnoser(user_query: str, chosen_model: str, exercise_format: str, sampling_count: str) -> tuple:
    num_samples = int("".join(filter(str.isdigit, sampling_count)))
    # Fetch the DiagnoserChain configuration.
    config = chain_configs["diagnoser"]

    # Instantiate DiagnoserChain using:
    # - A fixed LLM for standardizing (gpt4o-mini)
    # - The user-selected model for diagnosis (overriding the default)
    chain_instance = config["class"](
        template_standardize=config["template_standardize"],
        template_diagnose=config["template_diagnose"],
        llm_standardize=config["llm_standardize"],  # Fixed: gpt4o-mini
        llm_diagnose=llms.get(chosen_model, config["llm_diagnose"])  # Override or fallback to default
    )
    responses = []
    for i in range(num_samples):
        response = await chain_instance.run(user_query, exercise_format)
        responses.append(response)
    # Fill missing responses (if any) up to 5 outputs.
    all_responses = responses + [""] * (5 - len(responses))
    # Return a tuple of exactly 5 responses.
    return tuple(all_responses)

async def run_distractors(user_query: str, model_choice: str) -> str:
    return await run_chain("distractors", {"user_query": user_query}, model_choice)

# -------------------------------
# Build the Gradio Interface
# -------------------------------
with gr.Blocks() as demo:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(label="Enter Password", type="password", placeholder="hunter2")
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:
        gr.Markdown("## Pick the tab for your task of choice below")
        # Dropdown for LLM selection.
        # Create a row for the control dropdowns
        with gr.Row():
            model_choice = gr.Dropdown(
                choices=list(llms.keys()),
                value="GPT-4o",
                label="Select LLM",
                interactive=True,
            )
            exercise_format = gr.Dropdown(
                choices=["Markdown", "XML", "Plaintext", "Raw (original)"],
                value="Markdown",
                label="Exercise Format",
                interactive=True,
            )
            sampling_count = gr.Dropdown(
                choices=["1", "2", "3", "4", "5"],
                value="1",
                label="Sampling Count 🚧",
                interactive=True,
            )
        # Set up a change callback so that if the user selects "Claude3.5", the exercise format updates to "XML"
        model_choice.change(
            fn=update_exercise_format,
            inputs=[model_choice],
            outputs=[exercise_format]
        )
        with gr.Tabs():
            with gr.TabItem("🩺 Validate exercise"):
                # Insert an HTML info icon with a tooltip at the top of the tab content.
                gr.HTML(
                    """
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 1.5em; cursor: help;" title="Validate exercise: Diagnoses potential issues for the given exercise(s).">
                            ℹ️ <i>← mouseover for more info</i>
                        </span>
                    </div>
                    """
                )
                diagnoser_input = gr.Textbox(label="Enter exercise(s) in any format", placeholder="Exercise body: <mc:exercise xmlns:mc= ...")
                diagnoser_button = gr.Button("Submit")
                diagnoser_response_1 = gr.Textbox(label="Response 1", interactive=False)
                diagnoser_response_2 = gr.Textbox(label="Response 2", interactive=False)
                diagnoser_response_3 = gr.Textbox(label="Response 3", interactive=False)
                diagnoser_response_4 = gr.Textbox(label="Response 4", interactive=False)
                diagnoser_response_5 = gr.Textbox(label="Response 5", interactive=False)
            with gr.TabItem("🤔 Generate distractors"):
                # Insert an HTML info icon with a tooltip at the top of the tab content.
                gr.HTML(
                    """
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 1.5em; cursor: help;" title="Generate more different distractors for the given exercise">
                            ℹ️
                        </span>
                    </div>
                    """
                )
                distractors_input = gr.Textbox(label="Enter exercise(s) in any format", placeholder="Stelling: Dit is een ..... voorbeeld van een stelling. A. Mooi B. Lelijk ...")
                distractors_button = gr.Button("Submit")
                gr.Markdown("**Response(s):**")
                distractors_responses = gr.Column()
            with gr.TabItem("🚧 Generate learning objectives"):
                # Insert an HTML info icon with a tooltip at the top of the tab content.
                gr.HTML(
                    """
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 1.5em; cursor: help;" title="Generate learning objectives for the given study text">
                            ℹ️
                        </span>
                    </div>
                    """
                )
                learning_objectives_input = gr.Textbox(label="Enter exercise(s) in any format", placeholder="<h3>Infusie en infuussystemen</h3> <h4>Inleiding</h4> ...")
                learning_objectives_button = gr.Button("Submit")
                gr.Markdown("**Response(s):**")
                learning_objectives_responses = gr.Column()

    # -------------------------------
    # Set Up Interactions
    # -------------------------------
    # Login button interaction.
    login_button.click(
        fn=auth_login,
        inputs=[password_input],
        outputs=[login_container, app_container, login_error]
    )

    diagnoser_button.click(
        fn=run_diagnoser,
        inputs=[diagnoser_input, model_choice, exercise_format, sampling_count],
        outputs=[
            diagnoser_response_1,
            diagnoser_response_2,
            diagnoser_response_3,
            diagnoser_response_4,
            diagnoser_response_5
        ]
    )

    distractors_button.click(
        fn=run_distractors,
        inputs=[distractors_input, model_choice, exercise_format, sampling_count],
        outputs=[distractors_responses]
    )

# Launch the app.
demo.launch()
