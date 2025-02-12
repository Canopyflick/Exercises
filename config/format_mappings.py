# format_mappings.py

# Intermediate plain processing
FORMAT_MAPPINGS_EXERCISES = {
    "Markdown": (
        "Please reformat in Markdown, following this example:\n"
        "**Theorie:**\n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "---\n\n"
        "**Vraag:**\n"
        "Wat is de meest passende definitie van eenzaamheid?\n\n"
        "1. Het gevoel geen connectie te hebben met anderen\n"
        "2. Regelmatig in je eentje zijn\n"
        "3. Beide bovenstaande\n"
        "4. Geen van bovenstaande\n\n"
        "**Correct antwoord:**\n"
        "1. Het gevoel geen connectie te hebben met anderen\n\n"
        "**Uitleg:**\n"
        "Connectie betekent verbinding."
    ),
    "XML": (
        "Please reformat in XML, following this example:\n"
        "<exercise>\n"
        "    <content>\n"
        "        <prompt>Theorie:\n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "Vraag:\n"
        "Wat is de meest passende definitie van eenzaamheid?</prompt>\n"
        "        <options>\n"
        "            <option id=\"1\">Het gevoel geen connectie te hebben met anderen</option>\n"
        "            <option id=\"2\">Regelmatig in je eentje zijn</option>\n"
        "            <option id=\"3\">Beide bovenstaande</option>\n"
        "            <option id=\"4\">Geen van bovenstaande</option>\n"
        "        </options>\n"
        "    </content>\n"
        "        <correct_answer>1</correct_answer>\n"
        "        <explanation>Connectie betekent verbinding.</explanation>\n"
        "</exercise>"
    ),
    "Plaintext": (
        "Please reformat in plain text, following this example:\n"
        "Theorie:\n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "Vraag:\n"
        "Wat is de meest passende definitie van eenzaamheid?\n\n"
        "1. Het gevoel geen connectie te hebben met anderen\n"
        "2. Regelmatig in je eentje zijn\n"
        "3. Beide bovenstaande\n"
        "4. Geen van bovenstaande\n\n"
        "Correct antwoord:\n"
        "1. Het gevoel geen connectie te hebben met anderen\n\n"
        "Extra info:\n"
        "Connectie betekent verbinding."
    )
}


FORMAT_MAPPINGS_STUDY_TEXTS = {
    "Markdown": (
        "Please reformat into Markdown."
    ),
    "XML": (
        """
        Please reformat into XML, use tags like <title></title> and <b></b>.
        """
    ),
    "Plaintext": (
        "Please reformat into neat plaintext, without any tags or other formatting."
    )
}

# Final processing
studytext_HTML = (
        """
        Please reformat into XML. The target conventions are:
        - always start with a title like this: <h3>TITLE</h3>;
        - subheadings are just in bold. Usually there won't be any subheadings though, just different paragraphs;
        - for bold text, use <strong></strong>;
        - divide the text up into <p></p>-blocks;
        - for lists, adhere to the following capitalization and interpunction rules:
        <p>This is an example list, pay attention to lowercase beginnings and final interpunction endings of each item:</p>
            <ul>
                <li>each item starts with lowercase;</li>
                <li>always. Even if it's several sentences long. Like this one;</li>
                <li>each item ends with a semicolon;</li>
                <li>except for the very latest item;</li>
                <li>that (this) final item, ends with a full-stop, a period.</li>
            </ul>
        """
)