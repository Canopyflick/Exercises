# main.py
import gradio as gr
import logging
from app.ui.diagnoser_tab import build_diagnoser_tab
from app.ui.distractors_tab import build_distractors_tab
from chains.diagnoser.runner import run_diagnoser
from chains.distractors.runner import run_distractors
from utils.auth import login as auth_login

logger = logging.getLogger(__name__)



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

        # --- Standardized Exercise/Studytext Display (Initially Invisible Because it's empty) ---
        standardized_format_display = gr.Markdown("", visible=True)

        gr.Markdown("## Pick the tab for your task of choice")

        with gr.Tabs():
            # Build Diagnoser tab
            (model_choice_diagnose,
             exercise_format_diagnose,
             sampling_count_diagnose,
             diagnoser_input,
             diagnoser_button,
             diagnoser_responses
            ) = build_diagnoser_tab()

            # Build Distractors tab
            (model_choice_distractors_1,
             model_choice_distractors_2,
             model_choice_distractors_3,
             exercise_format_distractors,
             sampling_count_distractors,
             distractors_input,
             distractors_button,
             distractors_responses,
             intermediate_distractors_specification,
             final_distractors_specification,
             ) = build_distractors_tab()

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
                # Create 5 Response textboxes
                distractors_responses = [
                    gr.Textbox(label=f"Response {i + 1}", interactive=False, visible=(i == 0))
                    for i in range(10)
                ]

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
        inputs=[diagnoser_input, model_choice_diagnose, exercise_format_diagnose, sampling_count_diagnose],
        outputs=diagnoser_responses + [standardized_format_display],
    )

    distractors_button.click(
        fn=run_distractors,
        inputs=[
            distractors_input,  # user query
            model_choice_distractors_1,
            model_choice_distractors_2,
            model_choice_distractors_3,
            exercise_format_distractors,
            sampling_count_distractors,
            intermediate_distractors_specification,
            final_distractors_specification,
        ],
        outputs=distractors_responses + [standardized_format_display],
    )

# Launch the app.
interface.launch()
