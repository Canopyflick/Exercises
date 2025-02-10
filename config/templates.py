# config/templates.py
from langchain_core.prompts.chat import ChatPromptTemplate

# Template to standardize the exercise description.
standardize_template = ChatPromptTemplate(
    messages=[
        ("system", "You reformat data on multiple choice exercises. Convert the given exercise(s) into a standardized format. {formatting_instructions}"),
        ("human", "{user_input}")
    ],
    input_variables=["user_input", "formatting_instructions"]
)

# Template to generate a diagnosis from the standardized exercise.
diagnose_template = ChatPromptTemplate(
    messages=[
        ("system", "Based on the given exercise, provide a detailed diagnosis of potential issues. What makes this exercise sub-par, worse than it could be, not yet perfect? Only give the diagnosis, no solutions."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
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
        If the issue is more nuanced, do some reasoning first, and give your diagnosis then."""),
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
        
        Your only focus is to accurately diagnose this issue, no need to provide a fix. If the correct answer in the given exercise clearly does or does not stand out, just give a short one-sentence diagnosis on this. 
        If the issue is more nuanced, do some reasoning first, and give your diagnosis then."""),
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
        Your only focus is to accurately diagnose this issue, no need to provide a fix. If all distractors in the given exercise clearly either are or aren't obviously incorrect, just give a short one-sentence diagnosis on this. 
        If the issue is more nuanced, share your reasoning about it first, and give your diagnosis then."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

template_diagnose_distractor_partially_correct = ChatPromptTemplate(
    messages=[
        ("system", """You analyze a multiple-choice exercise to detect distractors that are 
        partially correct. Some answer choices may contain elements of truth, leading to 
        ambiguity. Identify such cases. Really stress-test them: is there a story you could tell where the distractor, in the context of this exercise, could be considered a (partially) correct answer?
        After this, consider if this is bad enough in the context of this question. It's fine if the correct answer is still obviously most correct, and some distractors that contain elements of truth. This is only a problem if the gap becomes too small. 
        As an intuition pump, ask this question: would there be any experts that would consider this distractor also a correct answer? If so, diagnose the problem. If not, it's fine.  
        Your only focus is to accurately diagnose this issue, no need to provide a fix. If all distractors in the given exercise clearly are or aren't unambiguously false, just give a short one-sentence diagnosis on this. 
        If the issue is more nuanced, do some reasoning first, and give your diagnosis then.
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
        3. A distractor answer option is too obviously false (it's useless, no student would ever pick it)
        4. A distractor answer option is actually also kinda correct (it's misleading, if a student picks it they're not 100% wrong) 
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
        Sometimes the diagnoses will be short and clear, but sometimes they will also be elaborate and view the issue from different angles. In that case, overweight the final sentence of the diagnosis. Here, usually the conclusion is drawn
        """),
        ("human", "{combined_diagnosis}")
    ],
    input_variables=["combined_diagnosis"]
)



template_distractors_brainstorm_1 = ChatPromptTemplate(
    messages=[
        ("system", "You are a brainstorming assistant. Based on the given multiple choice exercise, come up with{intermediate_distractors_specification}additional high-quality distractors: "
                   "alternative answer options that are not correct, yet also not so implausible that even poorly informed students would immediately dismiss them. Make sure to use the same language as the existing exercise."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)

template_distractors_brainstorm_2 = ChatPromptTemplate(
    messages=[
        ("system", "You are a brainstorming assistant. Based on the given multiple choice exercise, come up with{intermediate_distractors_specification}additional high-quality distractors: "
                   "alternative answer options that are not correct, yet not so implausible that even poorly informed students would immediately dismiss them. Go about this very methodically: "
                   "Really try to think outside of the box and get creative here, providing potential alternative distractors across a wide range of options. "
                   "Before you present your final selection, take your time to really consider the entire solution space, weighing your different ideas an options, then to list the distractors. Make sure to use the same language as the existing exercise."),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise", "intermediate_distractors_specification"]
)


template_consolidate_distractors  = ChatPromptTemplate(
    messages=[
        ("system", "You are given several lists of potential distractors (answer options to a multiple choice exercise), that need to be consolidated into one list. "
                   "Filter out duplicates, do some logical sorting among them, and just return one plain list{final_distractors_specification}. "
                   "Only focus on the distractors (answer options) themselves, ignore any reasoning about them. Return only the list, nothing else. Format the list without numbering or bullet points, just put every distractor on its own line. Use the same language as the existing exercise. "),
        ("human", "For context, this is the exercise that the distractors are about:\n "
                  "{standardized_exercise} "
                  "Here are the lists:\n "
                  "{brainstorm_outputs} ")
    ],
    input_variables=["standardized_exercise", "brainstorm_outputs", "final_distractors_specification"]
)

