import gradio as gr
from chains.learning_objectives_generator.runner import run_learning_objectives_generator
from config.llm_config import llms

def build_write_fluster_tab():
    with gr.TabItem("✍️ Write Fluster"):
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Generates one exercise set (one fluster) of 3 exercises for the given learning objective">
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
                value="GPT-4o-mini (low temp)",
                label="LLM 2"
            )


        exercises_input = gr.Textbox(label="Enter a learning objective", value="De student weet dat")
        write_fluster_button = gr.Button("Generate Fluster")

        # 2×2 textboxes => 4 total
        # For clarity:
        #   row 1 => (box_0, box_1)
        #   row 2 => (box_2, box_3)
        with gr.Row():
            box_0 = gr.Textbox(label="Prompt A + LLM 1", interactive=False)
            box_1 = gr.Textbox(label="Prompt A + LLM 1", interactive=False)
        with gr.Row():
            box_2 = gr.Textbox(label="Prompt A + LLM 2", interactive=False)
            box_3 = gr.Textbox(label="Prompt A + LLM 2", interactive=False)



    # Return references if needed
    return (model_choice_1,
            model_choice_2,
            exercises_input,
            write_fluster_button,
            [box_0, box_1, box_2, box_3],
    )
