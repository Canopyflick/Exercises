# app.py
import gradio as gr
import os
import asyncio
import logging

from config.exercise_standardizer import standardize_exercise
from utils.auth import login as auth_login
from config.chain_configs import chain_configs
from config.llm_config import llms

logger = logging.getLogger(__name__)

# --- Callback to update the exercise format dropdown based on LLM selection ---
def update_exercise_format(selected_model: str):
    # When "Claude3.5" is selected, default the format to XML; otherwise, default to Markdown.
    if "Claude" in selected_model:
        return gr.update(value="XML")
    else:
        return gr.update(value="Plaintext")



# Async wrappers for each chain.
async def run_diagnoser(user_query: str, model_choice_validate: str, exercise_format_validate: str, sampling_count_validate: str) -> tuple:
    """
    Diagnose exercise(s) in parallel using a configured DiagnoserChain.

    This function:
      1. Standardizes the exercise text once using the chain's fixed LLM.
      2. Instantiates the DiagnoserChain with a user-selected diagnosing LLM.
      3. Performs multiple diagnoses in parallel (as many times as `sampling_count_validate`).
      4. Pads the results to ensure a fixed number of output fields (10).

    Args:
        user_query (str): Raw exercise data submitted by the user.
        model_choice_validate (str): The key/name of the chosen LLM for diagnosing.
        exercise_format_validate (str): The desired format for standardizing the exercise.
        sampling_count_validate (str): A string representing how many diagnoses to run concurrently (e.g., "3").

    Returns:
        tuple: A tuple of length 10, each containing a diagnosis result (or empty string if not enough samples).
    """
    # figure out how many times to run
    num_samples = int("".join(filter(str.isdigit, sampling_count_validate)))

    # Fetch the DiagnoserChain configuration.
    config = chain_configs["diagnoser"]

    # 1) Standardize the user query exactly once
    standardized_exercise = await standardize_exercise(
        user_query,
        exercise_format_validate,
        config["template_standardize"],  # Only if you kept them in config
        config["llm_standardize"]
    )

    # 2) Instantiate the DiagnoserChain using the user-selected LLM for diagnosing
    chain_instance = config["class"](
        templates_diagnose=config["templates_diagnose"],
        llm_diagnose=llms.get(model_choice_validate, config["llm_diagnose"]),
        template_diagnose_scorecard=config["template_diagnose_scorecard"],
        llm_4o_mini=config["llm_4o_mini"],
        llm_4o=config["llm_4o"]
    )

    # 3) Run the multiple samples in parallel
    # Create a short helper that does only the "diagnose" steps:
    tasks = [
        chain_instance.diagnose_only(standardized_exercise)
        for _ in range(num_samples)
    ]
    # run concurrently
    responses = await asyncio.gather(*tasks)

    # pad up to 10 if needed
    all_responses = list(responses) + [""] * (10 - len(responses))

    # Return a tuple of exactly 5 responses.
    return tuple(all_responses)


async def run_distractors(
    user_query: str,
    model_choice_distractors_1: str,
    model_choice_distractors_2: str,
    exercise_format_distractors: str,
    sampling_count_distractors: str,
    intermediate_distractors_specification: str,
    final_distractors_specification: str,
) -> tuple:
    """
    Generate distractors by running the DistractorsChain multiple times in parallel.

    1. Standardizes the exercise text once using a fixed LLM.
    2. Constructs a DistractorsChain, where the user can pick two LLMs
       (e.g. one low-temp, one mid-temp) for parallel brainstorming steps.
    3. Invokes the chain ``num_samples`` times in parallel (based on ``sampling_count_distractors``),
       each time producing one consolidated distractors output.
    4. Pads the results to fill 10 output fields.
    """
    # 0) Parse how many concurrent runs (samples) we want
    num_samples = int("".join(filter(str.isdigit, sampling_count_distractors)))
    # Fetch the DistractorsChain configuration.
    config = chain_configs["distractors"]

    # 1) Standardize the user query exactly once
    standardized_exercise = await standardize_exercise(
        user_query,
        exercise_format_distractors,
        config["template_standardize"],
        config["llm_standardize"]
    )

    # 2) Build the DistractorsChain instance
    chain_instance = config["class"](
        template_distractors_brainstorm_1=config["template_distractors_brainstorm_1"],
        template_distractors_brainstorm_2=config["template_distractors_brainstorm_2"],
        llm_brainstorm_1=llms.get(model_choice_distractors_1, config["llm_brainstorm_1"]),  # User-selected (low and high temp GPT-4o by default)
        llm_brainstorm_2=llms.get(model_choice_distractors_2, config["llm_brainstorm_2"]),
        template_consolidate=config["template_consolidate"],
        llm_consolidate=config["llm_consolidate"],
    )

    # 3) Create N tasks in parallel (one full distractor generation pipeline per sample)
    tasks = [
        chain_instance.run(standardized_exercise, intermediate_distractors_specification, final_distractors_specification) for _ in range(num_samples)
    ]
    results = await asyncio.gather(*tasks)

    # 4) Pad up to 10 outputs to correspond to 10 response fields
    all_responses = list(results) + [""] * (10 - len(results))

    return tuple(all_responses)



# A generic async runner for simple chains (currently not used)
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
        content = result.content if hasattr(result, "content") else result
        # Replace literal "\n" (backslash-n) with actual newline characters.
        formatted_content = content.replace("\\n", "\n")

        logger.info(f"Chain '{chain_name}' executed successfully.")

        return formatted_content


    except Exception as e:
        logger.error(f"Error in run_chain for '{chain_name}': {e}")
        return f"Error: {e}"


# -------------------------------
# Build the Gradio Interface
# -------------------------------
with gr.Blocks() as interface:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(label="Enter Password", type="password", placeholder="hunter2")
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:
        gr.Markdown("## Pick the tab for your task of choice")

        with gr.Tabs():
            with gr.TabItem("🩺 Diagnose exercise"):
                # Insert an HTML info icon with a tooltip at the top of the tab content.
                gr.HTML(
                    """
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 1.5em; cursor: help;" title="Diagnose exercise for the 4 most common issues. The Exercise Format dropdown decides into what standardized format the exercise is converted initially for intermediate processing, to ensure reliable performance and consistent results. Claude typically works better with XML, OpenAI better with markdown. Sampling count = amount of responses.">
                            ℹ️ <i>←</i>
                        </span>
                    </div>
                    """
                )

                # Create a row for the control dropdowns: LLM selection, exercise format, sampling count etc.
                with gr.Row():
                    model_choice_validate = gr.Dropdown(
                        choices=list(llms.keys()),
                        value="GPT-4o (low temp)",
                        label="Select LLM",
                        interactive=True,
                    )
                    exercise_format_validate = gr.Dropdown(
                        choices=["Markdown", "XML", "Plaintext", "Raw (input unconverted)"],
                        value="Markdown",
                        label="Exercise Format (for intermediate processing",
                        interactive=True,
                    )
                    sampling_count_validate = gr.Dropdown(
                        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                        value="1",
                        label="Response Count",
                        interactive=True,
                    )
                # Set up a change callback so that if the user selects any model with "Claude" in the name, the exercise format updates to "XML"
                model_choice_validate.change(
                    fn=update_exercise_format,
                    inputs=[model_choice_validate],
                    outputs=[exercise_format_validate]
                )

                diagnoser_input = gr.Textbox(label="Enter exercise in any format", placeholder="Exercise body: <mc:exercise xmlns:mc= ...")
                diagnoser_button = gr.Button("Submit")
                diagnoser_response_1 = gr.Textbox(label="Response 1", interactive=False)
                diagnoser_response_2 = gr.Textbox(label="Response 2", interactive=False)
                diagnoser_response_3 = gr.Textbox(label="Response 3", interactive=False)
                diagnoser_response_4 = gr.Textbox(label="Response 4", interactive=False)
                diagnoser_response_5 = gr.Textbox(label="Response 5", interactive=False)
                diagnoser_response_6 = gr.Textbox(label="Response 6", interactive=False)
                diagnoser_response_7 = gr.Textbox(label="Response 7", interactive=False)
                diagnoser_response_8 = gr.Textbox(label="Response 8", interactive=False)
                diagnoser_response_9 = gr.Textbox(label="Response 9", interactive=False)
                diagnoser_response_10 = gr.Textbox(label="Response 10", interactive=False)


            with gr.TabItem("🤔 Brainstorm distractors"):
                # Insert an HTML info icon with a tooltip at the top of the tab content.
                gr.HTML(
                    """
                    <div style="margin-bottom: 10px;">
                        <span style="font-size: 1.5em; cursor: help;" title="Generate alternative distractors for the given exercise. Works with 2x2 brainstorming prompts (2 approaches, each using LLM 1 & LLM 2 once) and a final consolidation prompt combining all results together to present to the user.">
                            ℹ️
                        </span>
                    </div>
                    """
                )

                # Create a row for the control dropdowns: LLM selection, exercise format, sampling count etc.
                with gr.Row():
                    model_choice_distractors_1 = gr.Dropdown(
                        choices=list(llms.keys()),
                        value="GPT-4o (low temp)",
                        label="LLM 1",
                        interactive=True,
                    )
                    model_choice_distractors_2 = gr.Dropdown(
                        choices=list(llms.keys()),
                        value="GPT-4o (mid temp)",
                        label="LLM 2",
                        interactive=True,
                    )
                    exercise_format_distractors = gr.Dropdown(
                        choices=["Markdown", "XML", "Plaintext", "Raw (original)"],
                        value="Plaintext",
                        label="Exercise Format",
                        interactive=True,
                    )
                    sampling_count_distractors = gr.Dropdown(
                        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                        value="1",
                        label="Response Count",
                        interactive=True,
                    )
                    intermediate_distractors_specification = gr.Dropdown(
                        choices=["", "2", "3", "4", "5", "6", "7", "8", "9", "10", "a few", "some", "a whole lot of", "a wide range of", "novel"],
                        value="8",
                        label="Brainstorm X intermediate distractors (done x4)",
                        interactive=True,
                    )
                    final_distractors_specification = gr.Dropdown(
                        choices=["all unique distractors", "the best distractors", "only the very best distractors", "4", "5", "6", "7", "8", "9", "10", "11", "12", "a few", "some", "a whole lot of",
                                 "a wide range of", "novel"],
                        value="all unique distractors",
                        label="Finally display X distractors",
                        interactive=True,
                    )
                # Set up a change callback so that if the user selects any model with "Claude" in the name, the exercise format updates to "XML"
                model_choice_distractors_1.change(
                    fn=update_exercise_format,
                    inputs=[model_choice_distractors_1],
                    outputs=[exercise_format_distractors]
                )
                
                distractors_input = gr.Textbox(label="Enter exercise(s) in any format", placeholder="Stelling: Dit is een ..... voorbeeld van een stelling. A. Mooi B. Lelijk ...")
                distractors_button = gr.Button("Submit")
                distractors_response_1 = gr.Textbox(label="Response 1", interactive=False)
                distractors_response_2 = gr.Textbox(label="Response 2", interactive=False)
                distractors_response_3 = gr.Textbox(label="Response 3", interactive=False)
                distractors_response_4 = gr.Textbox(label="Response 4", interactive=False)
                distractors_response_5 = gr.Textbox(label="Response 5", interactive=False)
                distractors_response_6 = gr.Textbox(label="Response 6", interactive=False)
                distractors_response_7 = gr.Textbox(label="Response 7", interactive=False)
                distractors_response_8 = gr.Textbox(label="Response 8", interactive=False)
                distractors_response_9 = gr.Textbox(label="Response 9", interactive=False)
                distractors_response_10 = gr.Textbox(label="Response 10", interactive=False)
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
                learning_objectives_input = gr.Textbox(label="Enter a study text in any format", placeholder="<h3>Infusie en infuussystemen</h3> <h4>Inleiding</h4> ...")
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
        inputs=[diagnoser_input, model_choice_validate, exercise_format_validate, sampling_count_validate],
        outputs=[
            diagnoser_response_1,
            diagnoser_response_2,
            diagnoser_response_3,
            diagnoser_response_4,
            diagnoser_response_5,
            diagnoser_response_6,
            diagnoser_response_7,
            diagnoser_response_8,
            diagnoser_response_9,
            diagnoser_response_10
        ]
    )

    distractors_button.click(
        fn=run_distractors,
        inputs=[distractors_input, model_choice_distractors_1, model_choice_distractors_2, exercise_format_distractors, sampling_count_distractors],
        outputs=[
            distractors_response_1,
            distractors_response_2,
            distractors_response_3,
            distractors_response_4,
            distractors_response_5,
            distractors_response_6,
            distractors_response_7,
            distractors_response_8,
            distractors_response_9,
            distractors_response_10
        ]
    )

# Launch the app.
interface.launch()
