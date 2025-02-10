# ui/common.py
import gradio as gr

# --- Callback to update the exercise format dropdown based on LLM selection ---
def update_exercise_format(selected_model: str):
    """
    When the user picks a new model:
    - If it has 'Claude' in the name, default format to XML.
    - Otherwise, default to Plaintext.
    """
    if "Claude" in selected_model:
        return gr.update(value="XML")
    else:
        return gr.update(value="Plaintext")


def update_response_textboxes_amount(sampling_count: str):
    """
    Dynamically show/hide Response textboxes based on sampling count.
    """
    # Convert string to integer
    num = int(sampling_count)

    # We'll return a list of 10 updates, one for each textbox.
    updates = []
    for i in range(10):
        if i < num:
            # Show and label (i+1)
            updates.append(gr.update(visible=True, label=f"Response {i+1}"))
        else:
            # Hide the rest
            updates.append(gr.update(visible=False, label=f"Response {i + 1}"))
    return updates
