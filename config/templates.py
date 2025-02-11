# config/templates.py
from langchain_core.prompts.chat import ChatPromptTemplate

# Template to standardize the exercise description.
standardize_template = ChatPromptTemplate(
    messages=[
        ("system", "You reformat a given multiple choice exercise into a standardized format. {formatting_instructions}\n\n"
                   "Only 3 elements are always mandatory:\n"
                   "1. A question or statement that starts with 'Vraag:' or 'Stelling:' (or their semantic equivalents in the language of the exercise).\n"
                   "2. A minimum of two answer options (in the spirit of 'multiple choice'), one of them the correct answer\n"
                   "3. An indication of what the correct answer is.\n\n"
                   "Always return an exercise with at least these mandatory elements. If any of the 3 elements are missing "
                   "in the input, do your educated best to make them up. Beyond the 3 mandatory elements, never make up any "
                   "new content that is not present in the given exercise. You should sometimes leave out certain content "
                   "however, if there are artifacts with the given exercise that don't contribute to it."),
        ("human", "Here's the given exercise:\n{user_input}")
    ],
    input_variables=["user_input", "formatting_instructions"]
)

template_diagnose_double_negation = ChatPromptTemplate(
    messages=[
        ("system", """Analyze a multiple-choice exercise for the presence of double negatives: either two negations in the question/statement itself, or a negation in the question/statement AND in an answer option. 
        Here are some examples of double negatives:
        
        <example 1>
        <exercise>
        Stelling  
        Expertfolio wordt niet aangeboden door ENI.  
        
        Keuzeopties:  
        1. Deze stelling is niet correct  
        2. Deze stelling is correct  
        
        Correct antwoord:  
        1. Deze stelling is niet correct
        </exercise>
        <double negative explanation>
        The statement itself contains one negation (wordt 'niet' aangeboden), and one answer option contains another (is 'niet' correct). Interpreted together, this forms a statement with a double negation ('het is niet correct dat Expertfolio niet wordt aangeboden' is een dubbele ontkenning).
        </double negative explanation>
        </example 1>
        
        <example 2>
        <exercise>
        Vraag
        Welk aspect hoort niet bij eenzaamheid?
        
        Keuzeopties:  
        1. Betekenisvolle relaties hebben
        2. Depressiviteit en angst
        3. Veel alleen zijn
        4. Geen lijfelijk contact hebben
        
        Correct antwoord:
        1. Betekenisvolle relaties hebben
        </exercise>
        <double negative explanation>
        The question itself contains one negation  (hoort 'niet' bij), and an answer option contains the second ('Geen' lijfelijk contact). Together, the resulting statement contains a double negation ('Geen lichamelijk contact hebben hoort niet bij eenzaamheid'). 
        </double negative explanation>
        </example 2>. 
        If it's obvious that there is or isn't a double negative in this exercise, just give a short one-sentence diagnosis on this. 
        If the issue is more nuanced, take more time to do some reasoning first, and give your diagnosis only after."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

template_diagnose_correct_answer_stands_out = ChatPromptTemplate(
    messages=[
        ("system", """You evaluate a multiple-choice exercise to determine if the correct answer 
        stands out too much compared to the distractors. If the correct answer is significantly 
        longer, more detailed, or structurally or grammatically different, this is undesirable. Identify such 
        cases. 
        Here are some examples of cases where the correct answer stands out:
        
        <example where the correct answer is much longer>
        <exercise>
        Theorie:  
        De volgende afbeelding komt uit een onderzoek over eenzaamheid dat in 2012 is uitgevoerd.  
        
        Vraag:  
        Bij welke groep komt eenzaamheid volgens dit onderzoek het vaakst voor?  
        
        1. Gehandicapten  
        2. Mantelzorgers  
        3. Mensen met langdurige psychische aandoeningen  
        4. Sporters  
        
        Correct antwoord:  
        3. Mensen met langdurige psychische aandoeningen.
        </exercise>
        <explanation how the correct answer stands out>
        Alle afleiders zijn 1 woord (kort), terwijl het correcte antwoord een zin is (duidelijk langer).
        </explanation how the correct answer stands out>
        </example where X>
        
        <example where the correct answer is grammatically different>
        <exercise>
        Vraag: Wat is alimentatie?

        1. Geld dat betaald moet worden na een scheiding 
        2. Een lening van de overheid  
        3. Een maandelijkse bijdrage aan liefdadigheid  
        4. Een belastingteruggave  
        
        Correct antwoord:  
        1. Geld dat betaald moet worden na een scheiding of als men niet meer samen is met de andere ouder van de kinderen.

        </exercise>
        <explanation how the correct answer stands out>
        Alle afleiders beginnen met "Een", maar het correcte antwoord begint anders.
        </explanation how the correct answer stands out>
        </example where the correct answer is grammatically different>
        
        Your only focus is to accurately diagnose this issue, no need to provide a fix. Really take your time to arrive at the correct diagnosis. 
        Do some reasoning first, and give your diagnosis then."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

# <example where X>
# <exercise>
# </exercise>
# <explanation how the correct answer stands out>
# </explanation how the correct answer stands out>
# </example where X>

template_diagnose_distractor_clearly_wrong = ChatPromptTemplate(
    messages=[
        ("system", """You assess a multiple-choice exercise to determine if any distractors 
        are clearly incorrect and therefore too easy to eliminate. Effective distractors should at least sound plausible to some students.
        Identify distractors that are too obviously wrong, such that even students that are completely uninformed about the topic can eliminate them.
        Your only focus is to accurately diagnose this issue, no need to provide a fix. Really take your time to arrive at the correct diagnosis. 
        Do some reasoning first, and give your diagnosis then."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

template_diagnose_distractor_partially_correct = ChatPromptTemplate(
    messages=[
        ("system", """You analyze a multiple-choice exercise to detect distractors that are 
        partially correct. Some answer choices may contain elements of truth, leading to 
        ambiguity. Identify such cases. Really stress-test them: is there a story you could tell where the distractors, in the context of this exercise, could be considered a (partially) correct answer?
        After this, consider if this is bad enough in the context of this question. It's fine if the correct answer is still obviously most correct, and some distractors that contain elements of truth. This is only a problem if the gap becomes too small. 
        As an intuition pump, ask this question: would there be any experts that would consider this distractors also a correct answer? If so, diagnose the problem. If not, it's fine.  
        Your only focus is to accurately diagnose this issue, no need to provide a fix. Really take your time to arrive at the correct diagnosis. 
        Do some reasoning first, and give your diagnosis then.
        """),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

diagnose_scorecard_template = ChatPromptTemplate(
    messages=[
        ("system", """You analyze the results of the diagnoses of 4 potential issues that multiple choice exercises sometimes have, and consolidate those into a very simple one-line visual scorecard that summarizes all issues' diagnoses, to show the results clearly in one overview. The diagnoses concern the following 4 potential issues:
        1. Double negatives (if the exercise contains something like 'to not not do something', this is undesirable)
        2. The correct multiple choice answer option stands out from the rest (this is a hint for the student)
        3. A distractors answer option is too obviously false (it's useless, no student would ever pick it)
        4. A distractors answer option is actually also kinda correct (it's misleading, if a student picks it they're not 100% wrong) 
        Use these two icons: 
        - ✅ means the diagnosis of the issue came back negative, so the issue is not present.
        - ❌ means the diagnosis of the issue came back positive, so the issue is present.
        (and a third icon if need be: - ❔ means the diagnosis is unclear)
        The scorecard should always look like this:
        <template>
        1. The exercise does not contain/contains a double negative: ✅/❌ -- 2. The correct answer does not/does stand out: ✅/❌ -- 3. None/Some of the distractors are too obviously false: ✅/❌ -- 4. None/Some of the distractors are actually also kinda correct: ✅/❌
        </template>
        <example 1>
        1. The exercise doesn't contain a double negative: ✅ -- 2. The correct answer does not stand out: ✅ -- 3. None of the distractors are too obviously false: ✅ -- 4. None of the distractors are actually also kinda correct: ✅
        </example 1>
        <example 2>
        1. The exercise doesn't contain a double negative: ✅ -- 2. The correct answer does stand out: ❌ -- 3. None of the distractors are too obviously false: ✅ -- 4. Some of the distractors are actually also kinda correct: ❌
        </example 2>
        <example 3>
        1. The exercise contains a double negative: ❌ -- 2. The correct answer does not stand out: ✅ -- 3. Some of the distractors are too obviously false: ❌ -- 4. None of the distractors are actually also kinda correct: ✅
        </example 3>
        Sometimes, diagnoses will be elaborate and first view the issue from different angles, considering both scenarios of passing and failing equally. In that case, overweight the final sentence of the diagnosis, because there you'll find the conclusion.
        """),
        ("human", "{combined_diagnosis}")
    ],
    input_variables=["combined_diagnosis"]
)



template_distractors_brainstorm_1 = ChatPromptTemplate(
    messages=[
        ("system", "Help me brainstorm. Based on the given multiple choice exercise, come up with{intermediate_distractors_specification}additional distractors: "
                   "alternative answer options that are not correct answers to the question, yet neither so implausible that even poorly informed students could immediately dismiss and eliminate them. (use the same language as the existing exercise)."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)

template_distractors_brainstorm_2 = ChatPromptTemplate(
    messages=[
        ("system", "Help me brainstorm answer options for a multiple choice exercise. Based on the given question, come up with{intermediate_distractors_specification}additional alternative distractors: "
                   "alternative answer options that are not correct, yet neither so implausible that even poorly informed students could immediately dismiss and eliminate them.\n\n"
                   "You can think about this as a spectrum between 'too correct' & 'too obviously false'. Or, in other words, a spectrum between two extreme ends that can be described as: "
                   "'An answer option that is not the correct answer to the question, yet extremely similar in meaning and scope to the correct answer, such that it's very debatable whether this answer option is not in fact also actually correct' & "
                   "'An answer option that is exceedingly unlikely, fantastical, off-base or ridiculous and therefore maximally obviously incorrect, such that no one who can read would think this could ever be the correct answer to the question'\n"
                   "Whether any particular distractors falls on the 'too correct' or 'too obviously incorrect' parts of the spectrum, is highly context-dependent. "
                   "This often depends on many aspects to do with question, for example its exact phrasing, specific (background) domain-knowledge related to the subject, "
                   "and assumptions about what test takers in the target group for this exercise already can be assumed to know or not know, and their intelligence.\n"
                   "In other words, it is not easy to pick distractors that are positioned inside the acceptable range on this spectrum. "
                   "Therefore, really try to go about your task here methodically: first establish the borders of the acceptable range of distractors by lingering there for a bit; taking into account the specific context of the given question, as follows.\n\n"
                   "Before drafting the final list, first come up with one or two faulty distractors, that are faulty in the sense that they would be júst too much on the 'too correct' side of the aforementioned spectrum.\n"
                   "Then, come up with one or two distractors that are júst faulty on the other side of that spectrum: júst too much on the side of 'too obviously false'.\n"
                   "As an intuition pump for the first category (distractors that are júst too correct), try to imagine experts in the question's domain discussing the answer option, and some of them arguing that the distractors would also be a valid answer to the given question. "
                   "As an intuition pump for the second category (distractors that are júst too obviously incorrect), try to image a student who is both generally stupid (bottom of his class) ánd uninformed about the given topic (didn't prepare for the test). Would even they júst so find it easy to eliminate the faulty distractors as clearly false?\n"
                   "Those are the two bounds of the spectrum range we aim to operate between during brainstorming.\n"
                   "So, through the above process of picking some júst faulty distractors in the context of the given question, both barely too correct and barely too obviously false, you establish the two bounds of acceptable distractors. When brainstorming, don't play it entirely safe though; when in doubt about where exactly on the spectrum the distractors would lie, just list the distractors you came up with anyway.\n\n"
                   "Next, in the brainstorming phase, it's most important that you get really creative and really try to think outside the box, to come up with the required potential alternative answer options to the exercise. We want to approach this task from all different angles, "
                   "to arrive at a varied selection of options, to serve as inspiration for a later stage of final selection (not now) to make the exercise the best it can be. For now, carry out the above-described prep in writing, then draft the list of{intermediate_distractors_specification} alternative distractors (in the same language as the existing exercise)."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)




template_consolidate_distractors  = ChatPromptTemplate(
    messages=[
        ("system", "You are given several lists of potential distractors (answer options to a multiple choice exercise), that need to be consolidated and/or trimmed down into one list. "
                   "Always at least filter out duplicates, do some logical sorting, and return one plain list{final_distractors_specification}. "
                   "Only focus on the distractors (answer options) themselves, don't carry over any reasoning about them. Return only the list. Format the list without numbering or bullet points, just put one distractors per line. Use the same language as the existing exercise.\n\n"
                   "For context, this is the exercise that the distractors are about:\n "
                   "{standardized_exercise}"),
        ("human", "Here are the lists:\n "
                  "{brainstorm_outputs}\n\n "
                  "--- end of lists ---\n\n"
                  "Now, your task is to return one plain list{final_distractors_specification}.")
    ],
    input_variables=["standardized_exercise", "brainstorm_outputs", "final_distractors_specification"]
)

