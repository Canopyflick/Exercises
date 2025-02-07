import os
import gradio as gr

CORRECT_PASSWORD = os.getenv("APP_PASSWORD")  # Ensure this is set in your environment

def login(password: str):
    """
    Verify the password. Returns a tuple to update the Gradio UI.
    """
    if password == CORRECT_PASSWORD:
        return gr.update(visible=False), gr.update(visible=True), ""
    else:
        return gr.update(visible=True), gr.update(visible=False), "❌ Incorrect password. Please try again or contact Ben."
