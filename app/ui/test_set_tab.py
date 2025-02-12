import gradio as gr

def build_test_set_tab():
    with gr.TabItem("❔ Test Set"):
        gr.HTML(
            """
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.5em; cursor: help;" title="Uncontaminated repository of exercises and study texts (not present in the prompts)">
                    ℹ️
                </span>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                subset_choice = gr.Dropdown(
                    choices=["Exercises ❔🚧", "Study Texts ️ℹ️🚧", "Show all ❔ℹ️"],
                    value="Both ❔ℹ️",
                    label="Subset Filter 🚧"
                )
            with gr.Column(scale=2):
                pass # only here to keep the first column in check: force narrower dropdown

        search_field = gr.Textbox(label="Text Search 🚧", placeholder="Dummy placeholder element, doesn't work")

        with open("test_samples.md", "r", encoding="utf-8") as file:
            markdown_content = file.read()

            gr.Markdown(markdown_content)


    # Return references
    return (subset_choice, search_field, )
