# format_mappings.py

FORMAT_MAPPINGS = {
    "Markdown": (
        "Please format the exercise in Markdown, similarly to this example:\n\n"
        "**Theorie**  \n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "---\n\n"
        "**Vraag**  \n"
        "Wat is de meest passende definitie van eenzaamheid?\n\n"
        "1. Het gevoel geen connectie te hebben met anderen  \n"
        "2. Regelmatig in je eentje zijn  \n"
        "3. Beide bovenstaande  \n"
        "4. Geen van bovenstaande  \n\n"
        "**Correct antwoord:**  \n"
        "1. Het gevoel geen connectie te hebben met anderen."
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
        "Please reformat in plain text, following this example:\n\n"
        "Theorie\n"
        "Eenzaamheid wordt door ieder persoon anders ervaren en is daarom subjectief.\n\n"
        "Vraag\n"
        "Wat is de meest passende definitie van eenzaamheid?\n\n"
        "1. Het gevoel geen connectie te hebben met anderen\n"
        "2. Regelmatig in je eentje zijn\n"
        "3. Beide bovenstaande\n"
        "4. Geen van bovenstaande\n\n"
        "Correct antwoord:\n"
        "1. Het gevoel geen connectie te hebben met anderen."
    )
}
