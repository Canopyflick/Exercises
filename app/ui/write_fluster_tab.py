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

            include_diagnosis = gr.Checkbox(
                label="Immediately diagnose & fix 🚧",
                value=False,
                info="Diagnose each exercise and fix if issues found?"
            )


        exercises_input = gr.Textbox(label="Enter a learning objective", value="De student weet dat")
        write_fluster_button = gr.Button("Generate Fluster")

        # Results section
        with gr.Column():
            # Original fluster results (2×2 grid)
            gr.Markdown("### Generated Fluster")
            with gr.Row():
                box_0 = gr.Textbox(label="Prompt A + LLM 1", interactive=False, lines=14)
                box_2 = gr.Textbox(label="Prompt A + LLM 2", interactive=False, lines=14)
            with gr.Row():
                box_1 = gr.Textbox(label="Prompt A + LLM 1", interactive=False, lines=14)
                box_3 = gr.Textbox(label="Prompt A + LLM 2", interactive=False, lines=14)

            # -- 2 side-by-side textboxes for diagnosis results (Track1 & Track3)
            with gr.Row():
                diagnosis_box_1 = gr.Textbox(label="Diagnoses: Track1 (3 exercises)", interactive=False,
                                             visible=True, lines=3)
                diagnosis_box_3 = gr.Textbox(label="Diagnoses: Track3 (3 exercises)", interactive=False,
                                             visible=True, lines=3)

            # -- 2 side-by-side textboxes for final fixed flusters (Track1 & Track3)
            with gr.Row():
                fixes_box_1 = gr.Textbox(label="Final Fixed Track1", interactive=False, visible=True, lines=14)
                fixes_box_3 = gr.Textbox(label="Final Fixed Track3", interactive=False, visible=True, lines=14)




    # Return all necessary references
    return (
        model_choice_1,
        model_choice_2,
        include_diagnosis,
        exercises_input,
        write_fluster_button,
        [box_0, box_1, box_2, box_3],
        diagnosis_box_1,
        diagnosis_box_3,
        fixes_box_1,
        fixes_box_3
    )
