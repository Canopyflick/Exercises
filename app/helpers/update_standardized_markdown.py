# app/helpers/update_standardized_markdown
import gradio as gr

dummy_state = gr.Textbox(visible=False, label="Most recent reformatting", show_label=False)

async def update_standardized_markdown(text_from_dummy):
    new_markdown = f"#### Most Recent Standardized Format\n{text_from_dummy}"
    return new_markdown
