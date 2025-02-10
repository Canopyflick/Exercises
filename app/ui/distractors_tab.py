# ui/distractors_tab.py
import gradio as gr
from common import update_response_textboxes_amount, update_exercise_format
from config.llm_config import llms


def build_distractors_tab():
    """
    Builds and returns the Diagnoser tab UI elements (and any references).
    """
    with gr.TabItem("🤔 Brainstorm distractors"):
        # Insert an HTML info icon with a tooltip at the top of the tab content.
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Generates alternative distractors for the given exercise in two stages. First, 2x2 brainstorming prompts (2 approaches, each using LLM 1 & LLM 2 once) generate a bunch of options, then a final consolidation prompt (using LLM 3) combines all results together for presentation below.\n\nFor both stages, prompts can be customized via dropdowns to influence the amount of distractors that will be generated during each (brainstormed and displayed).\n5-6 LLM calls per final response.">
                    ℹ️
                </span>
            </div>
            """
        )

        # Create a row for the control dropdowns: LLM selection, exercise format, sampling count etc.
        with gr.Row():
            model_choice_distractors_1 = gr.Dropdown(
                choices=list(llms.keys()),
                value="GPT-4o (mid temp)",
                label="LLM 1 - for brainstorming",
                interactive=True,
            )
            model_choice_distractors_2 = gr.Dropdown(
                choices=list(llms.keys()),
                value="Claude 3.5 (mid temp)",
                label="LLM 2 - for brainstorming",
                interactive=True,
            )
            exercise_format_distractors = gr.Dropdown(
                choices=["Markdown", "XML", "Plaintext", "Raw (input not reformatted)"],
                value="Plaintext",
                label="Exercise Reformat",
                interactive=True,
            )
            intermediate_distractors_specification = gr.Dropdown(
                choices=[" ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ", " 10 ", " a few ", " some ",
                         " a whole lot of ", " a wide range of ", " novel "],
                value=" 8 ",
                label="Brainstorm X distractors x4",
                interactive=True,
            )
            model_choice_distractors_3 = gr.Dropdown(
                choices=list(llms.keys()),
                value="GPT-4o (low temp)",
                label="LLM 3 - for consolidation",
                interactive=True,
            )
            final_distractors_specification = gr.Dropdown(
                choices=[" ", " of all unique distractors", " of the top 5", " of the best distractors",
                         " of only the very best", " of the best 4", " of the best 5", " of the best 6",
                         " of the best 7", " of the best 8", " of the best 9", " of the best 10", " of the best 11",
                         " of the best 12", " of a few of them", " of some of them", " of most of them",
                         " of a wide range of", " of the 3 worst"],
                value=" of all unique distractors",
                label="Finally display X distractors",
                interactive=True,
            )
            sampling_count_distractors = gr.Dropdown(
                choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                value="1",
                label="Response Count",
                interactive=True,
            )

        distractors_input = gr.Textbox(label="Enter exercise(s) in any format",
                                       placeholder="Stelling: Dit is een ..... voorbeeld van een stelling. A. Mooi B. Lelijk ...")
        distractors_button = gr.Button("Submit")

        # Create 10 Response textboxes
        distractors_responses = [
            gr.Textbox(label=f"Response {i + 1}", interactive=False, visible=(i == 0))
            for i in range(10)
        ]


        # Set up a change callback so that if the user selects any model with "Claude" in the name, the exercise format updates to "XML"
        model_choice_distractors_1.change(
            fn=update_exercise_format,
            inputs=[model_choice_distractors_1],
            outputs=[exercise_format_distractors]
        )

        # Callback to show/hide Response textboxes
        sampling_count_distractors.change(
            fn=update_response_textboxes_amount,
            inputs=[sampling_count_distractors],
            outputs=distractors_responses
        )

    return()