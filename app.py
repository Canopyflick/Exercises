import gradio as gr
import openai
import os

# Load secrets
CORRECT_PASSWORD = os.getenv("APP_PASSWORD")  # Set this in Hugging Face Spaces secrets
openai.api_key = os.getenv("OPENAI_API_KEY")     # Also store securely

client = openai.OpenAI()  # ✅ New format


# -------------------------------
# Define Functions for App Logic
# -------------------------------

def login(password):
    """
    Check the submitted password.
    If correct, hide the login container and show the main app.
    Otherwise, return an error message.
    """
    if password == CORRECT_PASSWORD:
        # Hide login page, show main app, and clear error message
        return gr.update(visible=False), gr.update(visible=True), ""
    else:
        # Remain on login page with an error message
        return gr.update(visible=True), gr.update(visible=False), "❌ Incorrect password. Please try again or contact Ben."

def diagnoser_query(user_query):
    """
    Process the Diagnoser query.
    (For now, simply pass the query to the OpenAI API.)
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        timeout=10,
        messages=[
            {
                "role": "user",
                "content": (
                    "What is wrong with this exercise? In other words, what about it should be improved? "
                    "What stands between it and a perfect exercise that couldn't be better? Don't give solutions yet, "
                    "only a diagnosis\n "
                    f"{user_query}"
                ),
            }
        ],
    )
    return response.choices[0].message.content

def distractors_query(user_query):
    """
    Process the Distractors brainstorm query.
    (For now, simply pass the query to the OpenAI API.)
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        timeout=10,
        messages=[{"role": "user", "content": user_query}]
    )
    return response.choices[0].message.content

# -------------------------------
# Build the Gradio Interface
# -------------------------------

with gr.Blocks() as demo:
    # --- Login Page ---
    with gr.Column(visible=True, elem_id="login_page") as login_container:
        gr.Markdown("## 🔒 Please Login")
        password_input = gr.Textbox(label="Enter Password", type="password", placeholder="Enter password to access the app")
        login_button = gr.Button("Login")
        login_error = gr.Markdown(value="")  # To display error messages

    # --- Main App (initially hidden) ---
    with gr.Column(visible=False, elem_id="main_app") as app_container:
        gr.Markdown("## Core Functionalities")
        # Use gr.Tabs for persistent states between functionalities
        with gr.Tabs():
            with gr.TabItem("Diagnoser"):
                gr.Markdown("### Diagnoser")
                diagnoser_input = gr.Textbox(label="Enter Diagnoser Query", placeholder="Type your query here...")
                diagnoser_button = gr.Button("Submit")
                diagnoser_output = gr.Textbox(label="Response", interactive=False)
            with gr.TabItem("Distractors brainstorm"):
                gr.Markdown("### Distractors brainstorm")
                distractors_input = gr.Textbox(label="Enter Brainstorm Query", placeholder="Type your query here...")
                distractors_button = gr.Button("Submit")
                distractors_output = gr.Textbox(label="Response", interactive=False)

    # -------------------------------
    # Set Up Interactions
    # -------------------------------

    # When the login button is clicked, check the password and update container visibility
    login_button.click(
        fn=login,
        inputs=[password_input],
        outputs=[login_container, app_container, login_error]
    )

    # Connect the Diagnoser functionality
    diagnoser_button.click(
        fn=diagnoser_query,
        inputs=[diagnoser_input],
        outputs=[diagnoser_output]
    )

    # Connect the Distractors brainstorm functionality
    distractors_button.click(
        fn=distractors_query,
        inputs=[distractors_input],
        outputs=[distractors_output]
    )

# Launch the app
demo.launch()