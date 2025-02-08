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

diagnose_double_negation_template = ChatPromptTemplate(
    messages=[
        ("system", """You analyze a multiple-choice exercise for the presence of double negatives. 
        Here are some examples of double negatives:
        
        <example 1>
        <exercise 1>
        Stelling  
        Expertfolio wordt niet aangeboden door ENI.  
        
        Keuzeopties:  
        1. Deze stelling is niet correct  
        2. Deze stelling is correct  
        
        Correct antwoord:  
        1. Deze stelling is niet correct
        </exercise 1>
        <double negative explanation>
        Een niet-correctvraag met 'niet' (het is niet correct dat Expertfolio niet wordt aangeboden) is een dubbele ontkenning.
        </double negative explanation>
        </example 1>
        
        <example 2>
        <exercise 2>
        Vraag
        Welk aspect hoort niet bij eenzaamheid?
        
        Keuzeopties:  
        1. Betekenisvolle relaties hebben
        2. Depressiviteit en angst
        3. Veel alleen zijn
        4. Geen lijfelijk contact hebben
        
        Correct antwoord:
        Het ontbreken van betekenisvolle relaties
        </exercise 2>
        <double negative explanation>
        In de vraag staat al 'niet'. In keuzeoptie 4 staat ook nog 'geen', dat is dus een dubbele ontkenning. 
        </double negative explanation>
        </example 2>. 
        If it's obvious that there is or isn't a double negative in this exercise, just give a short one-sentence diagnosis on this. 
        If you're not quite sure, do some reasoning first, and give your diagnosis then."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

diagnose_correct_answer_stands_out_template = ChatPromptTemplate(
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
        If you're not quite sure, do some reasoning first, and give your diagnosis then."""),
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

diagnose_distractor_clearly_wrong_template = ChatPromptTemplate(
    messages=[
        ("system", """You assess a multiple-choice exercise to determine if any distractors 
        are clearly incorrect and therefore too easy to eliminate. Effective distractors should 
        be plausible but incorrect. 
        Identify distractors that are obviously wrong, such that even students that are completely uninformed about the topic can eliminate them.
        Your only focus is to accurately diagnose this issue, no need to provide a fix. If all distractors in the given exercise clearly are or aren't obviously incorrect, just give a short one-sentence diagnosis on this. 
        If you're not quite sure, do some reasoning first, and give your diagnosis then."""),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

diagnose_distractor_partially_correct_template = ChatPromptTemplate(
    messages=[
        ("system", """You analyze a multiple-choice exercise to detect distractors that are 
        partially correct. Some answer choices may contain elements of truth, leading to 
        ambiguity. Identify such cases. Really stress-test them: is there a story you could tell where the distractor, in the context of this exercise, could be considered a (partially) correct answer?
        Your only focus is to accurately diagnose this issue, no need to provide a fix. If all distractors in the given exercise clearly are or aren't unambiguously false, just give a short one-sentence diagnosis on this. 
        If you're not quite sure, do some reasoning first, and give your diagnosis then.
        """),
        ("human", "{standardized_exercise}")
    ],
    input_variables=["standardized_exercise"]
)

# Template for the distractors brainstorm
distractors_template = ChatPromptTemplate(
    messages=[
        ("system", "You are a brainstorming assistant. Based on the given multiple choice exercise, come up with 10 additional distractors: "
                   "alternative answer options that are not correct, yet plausible enough that a poorly informed student might pick them. "
                   "Vary the degree of 'almost correctness' and 'clearly incorrectness' between them to provide a wide range of options."),
        ("human", "{user_input}")
    ],
    input_variables=["standardized_exercise"]
)
