# main.py
import gradio as gr
import logging

from app.ui.common import log_dropdown_choice
from app.ui.diagnoser_tab import build_diagnoser_tab
from app.ui.distractors_tab import build_distractors_tab
from app.ui.learning_objectives_tab import build_learning_objectives_tab
from app.ui.prompts_tab import build_prompts_tab
from app.ui.test_set_tab import build_test_set_tab
from app.ui.write_fluster_tab import build_write_fluster_tab
from chains.diagnoser.runner import run_diagnoser
from chains.distractors.runner import run_distractors
from chains.exercises.runner import run_fluster
from chains.learning_objectives_generator.runner import run_learning_objectives_generator
from utils.auth import login as auth_login

logger = logging.getLogger(__name__)



# -------------------------------
# Build the Gradio Interface
# -------------------------------
with gr.Blocks() as interface:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(
            label="Enter Password",
            type="password",
            placeholder="hunter2",
            container=True
        )
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:

        # --- Standardized Exercise/Study text Display (Initially Invisible Because it's empty) ---
        # A row for Title & the standardized text & copy button
        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown("")
            with gr.Column(scale=5):
                standardized_format_display = gr.Textbox(
                    info="",
                    label="",
                    show_label=False,
                    show_copy_button=True,
                    placeholder="will show most recent reformatting result",
                    lines=1,
                    max_lines=10,
                    interactive=False,
                    container=False
                )

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


            # Build Learning Objectives Generator tab
            (model_choice_LO_1,
             model_choice_LO_2,
             text_format,
             studytext_input,
             learning_objectives_button,
             [LO_box_0, LO_box_1, LO_box_2, LO_box_3]
             ) = build_learning_objectives_tab()

            # Build write_fluster tab
            (model_choice_fluster_1,
             model_choice_fluster_2,
             exercises_input,
             write_fluster_button,
             [fluster_box_0, fluster_box_1, fluster_box_2, fluster_box_3],
             ) = build_write_fluster_tab()

            # Empty separator
            with gr.TabItem("", visible=True, scale=3):
                pass

            # Build Prompts tab
            (pipeline_choice,
             search_field_prompts,
             ) = build_prompts_tab()

            # Build Test Set tab
            (subset_choice,
             search_field_test_set,
             ) = build_test_set_tab()

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

    learning_objectives_button.click(
        fn=run_learning_objectives_generator,  # Our async generator
        inputs=[studytext_input, model_choice_LO_1, model_choice_LO_2, text_format],
        outputs=[LO_box_0, LO_box_1, LO_box_2, LO_box_3, standardized_format_display],
        queue=True,
        api_name=None,
        # or "stream=True" depending on your version of Gradio
    )

    write_fluster_button.click(
        fn=run_fluster,  # async generator
        inputs=[exercises_input, model_choice_fluster_1, model_choice_fluster_2],
        outputs=[fluster_box_0, fluster_box_1, fluster_box_2, fluster_box_3],  # fill the 4 textboxes
        api_name=None,
        queue=True,
    )

    pipeline_choice.change(fn=log_dropdown_choice, inputs=pipeline_choice, outputs=[])
    subset_choice.change(fn=log_dropdown_choice, inputs=subset_choice, outputs=[])

# Launch the app.
interface.launch()
