# ui/diagnoser_tab.py
import gradio as gr
from config.llm_config import llms
from common import update_exercise_format, update_response_textboxes_amount


def build_diagnoser_tab():
    """
    Builds and returns the Diagnoser tab UI elements (and any references).
    """
    with gr.TabItem("🩺 Diagnose exercise"):
        # Insert an HTML info icon with a tooltip at the top of the tab content.
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Diagnoses exercise for their 4 most common issues.\n\nThe exercise format dropdown decides into what standardized format the exercise is converted initially for intermediate processing, to ensure reliable performance irrespective of source format.\nAnthropic models typically work better with XML, OpenAI's with markdown.\n\nResponse count is the amount of times a final response will be generated in the fields below (5-6 LLM queries for each).">
                    ℹ️ <i>←</i>
                </span>
            </div>
            """
        )

        # Create a row for the control dropdowns: LLM selection, exercise format, sampling count etc.
        with gr.Row():
            model_choice_diagnose = gr.Dropdown(
                choices=list(llms.keys()),
                value="GPT-4o (low temp)",
                label="Select LLM",
                interactive=True,
            )
            exercise_format_diagnose = gr.Dropdown(
                choices=["Markdown", "XML", "Plaintext", "Raw (input not reformatted)"],
                value="Markdown",
                label="Exercise Reformat",
                interactive=True,
            )
            sampling_count_diagnose = gr.Dropdown(
                choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                value="1",
                label="Response Count",
                interactive=True,
            )

        # The user input
        diagnoser_input = gr.Textbox(label="Enter exercise in any format",
                                     placeholder="Exercise body: <mc:exercise xmlns:mc= ...")
        # A button to run the chain
        diagnoser_button = gr.Button("Submit")

        # Create 10 Response textboxes
        diagnoser_responses = [
            gr.Textbox(label=f"Response {i + 1}", interactive=False, visible=(i == 0))
            for i in range(10)
        ]

        # Set up a change callback so that if the user selects any model with "Claude" in the name, the exercise format updates to "XML"
        model_choice_diagnose.change(
            fn=update_exercise_format,
            inputs=[model_choice_diagnose],
            outputs=[exercise_format_diagnose]
        )

        # Callback to show/hide Response textboxes
        sampling_count_diagnose.change(
            fn=update_response_textboxes_amount,
            inputs=[sampling_count_diagnose],
            outputs=diagnoser_responses
        )

    return (
        model_choice_diagnose,
        exercise_format_diagnose,
        sampling_count_diagnose,
        diagnoser_input,
        diagnoser_button,
        diagnoser_responses
    )