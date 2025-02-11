# format_mappings.py

# Intermediate plain processing
FORMAT_MAPPINGS_EXERCISES = {
    "Markdown": (
        "Please reformat in Markdown, following this example:\n"
        "**Theorie:**  \n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "---\n\n"
        "**Vraag:**  \n"
        "Wat is de meest passende definitie van eenzaamheid?\n\n"
        "1. Het gevoel geen connectie te hebben met anderen  \n"
        "2. Regelmatig in je eentje zijn  \n"
        "3. Beide bovenstaande  \n"
        "4. Geen van bovenstaande  \n\n"
        "**Correct antwoord:**  \n"
        "1. Het gevoel geen connectie te hebben met anderen"
    ),
    "XML": (
        "Please reformat in XML, following this example:\n"
        "<exercise>\n"
        "    <content>\n"
        "        <question>Theorie:\n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "Vraag:\n"
        "Wat is de meest passende definitie van eenzaamheid?</question>\n"
        "        <choices>\n"
        "            <choice id=\"1\">Het gevoel geen connectie te hebben met anderen</choice>\n"
        "            <choice id=\"2\">Regelmatig in je eentje zijn</choice>\n"
        "            <choice id=\"3\">Beide bovenstaande</choice>\n"
        "            <choice id=\"4\">Geen van bovenstaande</choice>\n"
        "        </choices>\n"
        "    </content>\n"
        "    <answer>\n"
        "        <correct-choice>1</correct-choice>\n"
        "        <explanation></explanation>\n"
        "    </answer>\n"
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
        "1. Het gevoel geen connectie te hebben met anderen"
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