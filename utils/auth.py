import os, asyncio
import gradio as gr

CORRECT_PASSWORD = os.getenv("APP_PASSWORD")  # Ensure this is set in your environment

def login(password: str):
    """
    Verify the password. Returns a tuple to update the Gradio UI.
    """
    if password == CORRECT_PASSWORD:
        return gr.update(visible=False), gr.update(visible=True), ""
    elif password == "hunter2":
        # Temporarily show the app
        yield gr.update(visible=False), gr.update(visible=False), "Nice try ❤️"
        await asyncio.sleep(1)
        yield gr.update(visible=False), gr.update(visible=True), "Nice try ❤️"
        await asyncio.sleep(4)
        yield gr.update(visible=True), gr.update(visible=False), "😈"
    else:
        return gr.update(visible=True), gr.update(visible=False), "❌ Incorrect password. Please try again or contact Ben."
