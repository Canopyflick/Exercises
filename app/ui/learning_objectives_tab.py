import gradio as gr
from chains.learning_objectives_generator.runner import run_learning_objectives_generator
from config.llm_config import llms

def build_learning_objectives_tab():
    with gr.TabItem("🧠 Identify Learning Objectives"):
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Generate learning objectives for the given study text">
                    ℹ️
                </span>
            </div>
            """
        )

        with gr.Row():
            # 2 dropdowns for the user-chosen LLMs:
            model_choice_1 = gr.Dropdown(
                choices=list(llms.keys()),
                value="o1 (high reasoning_effort)",
                label="LLM 1"
            )
            model_choice_2 = gr.Dropdown(
                choices=list(llms.keys()),
                value="o3-mini (high reasoning_effort)",
                label="LLM 2"
            )
            text_format = gr.Dropdown(
                    choices=["Markdown", "XML", "Plaintext", "Raw (input not reformatted)"],
                    value="Markdown",
                    label="Studytext Reformat",
                    interactive=True,
            )

        studytext_input = gr.Textbox(label="Enter a study text in any format", placeholder="<h3>Infusie en infuussystemen</h3> <h4>Inleiding</h4> ...")
        learning_objectives_button = gr.Button("Identify LOs")

        # 2×2 textboxes => 4 total
        # For clarity: 
        #   row 1 => (box_0, box_1) 
        #   row 2 => (box_2, box_3)
        with gr.Row():
            box_0 = gr.Textbox(label="Prompt A + LLM 1", interactive=False)
            box_1 = gr.Textbox(label="Prompt B + LLM 1", interactive=False)
        with gr.Row():
            box_2 = gr.Textbox(label="Prompt A + LLM 2", interactive=False)
            box_3 = gr.Textbox(label="Prompt B + LLM 2", interactive=False)



    # Return references if needed
    return (model_choice_1,
            model_choice_2,
            text_format,
            studytext_input,
            learning_objectives_button,
            [box_0, box_1, box_2, box_3])
