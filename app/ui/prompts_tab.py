import gradio as gr
from chains.learning_objectives_generator.runner import run_learning_objectives_generator
from config.llm_config import llms

def build_prompts_tab():
    with gr.TabItem("🗒🚧️ See Prompts"):
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Behind-the-scenes prompt perusing at your leisure">
                    ℹ️
                </span>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                pipeline_choice = gr.Dropdown(
                    choices=["Exercise Diagnosis 🩺", "Distractors Brainstorm 🤔", "Learning Objectives Identification 🧠", "ALL OF THEM ✨", ],
                    value="Exercise Diagnosis 🩺",
                    label="Tasks Pipelines"
                )
            with gr.Column(scale=2):
                pass # only here to keep the first column in check: force narrower dropdown

        gr.HTML = gr.Textbox(label="Text Search 🚧", placeholder="Dummy placeholder, doesn't work (yet?)")


    # Return references
    return (pipeline_choice)
