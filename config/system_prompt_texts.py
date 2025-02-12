# config/prompt_texts.py

template_standardize_exercise_text = """ 
"""

template_standardize_studytext_text = """ 
"""

template_diagnose_double_negation_text = """
Analyze a multiple-choice exercise (Question- or Statement-type) for the presence of double negatives: either two negations in the question/statement itself, or a negation in the question/statement AND in an answer option. 
Here are some examples of double negatives:

<example>
    <exercise>
        <prompt>
            <type>Vraag</type>
            <text>Wat is geen veel voorkomend symptoom (volgens de enquêteuitslag) van niet gelukkig zijn?</text>
        </prompt>
        
        <options>
            1. Gezondheidsproblemen
            2. Weinig tijd voor ontspanning
            3. Vaak alleen zijn
            4. Veel te doen hebben op je werk
        </options>
        
        <correct_answer>4</correct_answer>
    </exercise>

    <double_negative>
        First negation: "Wat is geen" in prompt
        Second negation: "van niet gelukkig zijn" in prompt
        
        Explanation: Two negations in the prompt ("geen" and "niet") form a double negation.
    </double_negative>
</example>

<example>
    <exercise>
        <prompt>
            <type>Stelling</type>
            <text>Expertfolio wordt niet aangeboden door ENI.</text>
        </prompt>
        
        <options>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </options>
        
        <correct_answer>1</correct_answer>
    </exercise>

    <double_negative>
        First negation: "wordt niet aangeboden" in prompt
        Second negation: "is niet correct" in option 1
        
        Explanation: Interpreted together (as the student would in their head, trying to pick the correct answer option), they form a statement with a double negation: "De stelling dat Expertfolio niet wordt aangeboden is niet correct"
    </double_negative>
</example>

<example>
    <exercise>
        <prompt>
            <type>Vraag</type>
            <text>Welk aspect hoort niet bij eenzaamheid?</text>
        </prompt>
        
        <options>
            1. Betekenisvolle relaties hebben
            2. Depressiviteit en angst
            3. Veel alleen zijn
            4. Geen lijfelijk contact hebben
        </options>
        
        <correct_answer>1</correct_answer>
    </exercise>

    <double_negative>
        First negation: "hoort niet bij" in prompt
        Second negation: "Geen lijfelijk contact" in option 4
        
        Explanation: Together, these create a double negative - "Geen lichamelijk contact 
        hebben hoort niet bij eenzaamheid"
    </double_negative>
</example>

If it's obvious that there is or isn't a double negative in this exercise, just give a short one-sentence diagnosis on this. 
If the issue is more nuanced, take more time to do some reasoning first, and give your diagnosis only then. 
"""

template_diagnose_correct_answer_stands_out_text = """
You evaluate a multiple-choice exercise to determine if the correct answer 
stands out inappropriately compared to the distractors. If the correct answer is significantly 
longer, much more specific, or grammatically or otherwise structurally different, this is undesirable. This is because any clear pattern in the answer options which distinguishes the correct answer from the other options, makes it easier for the students to guess correctly regardless of their factual knowledge. So, we are looking for cases where the correct answer differs from the rest in a cosmetic, meta-, visual or otherwise superficial way, which doesn't require factual understanding to spot. It is your task to diagnose such 
cases. 
Here are some examples of cases where the correct answer stands out inappropriately:

<examples>
    <example>
        <exercise>
            <context>
                De volgende afbeelding komt uit een onderzoek over eenzaamheid dat in 2012 is uitgevoerd.
            </context>
            
            <prompt>
                <type>Vraag</type>
                <text>Bij welke groep komt eenzaamheid volgens dit onderzoek het vaakst voor?</text>
            </prompt>
            
            <options>
                1. Gehandicapten
                2. Mantelzorgers
                3. Mensen met langdurige psychische aandoeningen
                4. Sporters
            </options>
            
            <correct_answer>3</correct_answer>
        </exercise>
    
        <answer_consistency_analysis>
            Issue: Length difference
            Pattern: All distractors are single words, while correct answer is a multi-word phrase
            Diagnosis: The longer length of the correct answer makes it stand out inappropriately
        </answer_consistency_analysis>
    </example>
    
    <example>
       <exercise>
           <prompt>
               <type>Vraag</type>
               <text>Wat is alimentatie?</text>
           </prompt>
           
           <options>
               1. Geld dat betaald moet worden na een scheiding
               2. Een lening van de overheid
               3. Een maandelijkse bijdrage aan liefdadigheid
               4. Een belastingteruggave
           </options>
           
           <correct_answer>1</correct_answer>
       </exercise>
    
       <answer_consistency_analysis>
           Issue: Grammatical structure difference
           Pattern: All distractors start with "Een", while correct answer starts with "Geld"
           Diagnosis: The different grammatical structure of the correct answer makes it stand out undesirably (a superficial pattern that could hint at the answer)
       </answer_consistency_analysis>
    </example>
    
    <example>
        <exercise>
            <prompt>
                <type>Vraag</type>
                <text>Welke onderwijskundige benadering wordt hier beschreven: "Leerlingen werken samen in kleine groepen en hebben elk een eigen rol en verantwoordelijkheid binnen de groep"?</text>
            </prompt>
            
            <options>
                1. Een activerende methode
                2. Jigsaw cooperative learning
                3. Benadering waarbij gedrag belangrijk is
                4. Leren als informatieverwerking
            </options>
            
            <correct_answer>2</correct_answer>
        </exercise>
    
        <answer_consistency_analysis>
            Issue: Scope difference
            Pattern: While distractors use general educational terms that could apply to many approaches, the correct answer uses a very specific named methodology
            Impact: The precise, technical term in the correct answer stands out against the much broader and high-level educational concepts in the distractors
        </answer_consistency_analysis>
    </example>
</examples>

Your only focus is to accurately diagnose this issue of an inappropriately different correct answer, no need to provide a fix. Really take your time to arrive at the correct diagnosis, weighing if the pattern is clear enough or not. 
Do some reasoning first, and give your diagnosis then.
"""

template_diagnose_distractor_clearly_wrong_text = """ 
"""

template_diagnose_distractor_partially_correct_text = """ 
"""

diagnose_scorecard_template_text = """ 
"""

template_distractors_brainstorm_1_text = """ 
"""

template_distractors_brainstorm_2_text = """ 
"""

template_consolidate_distractors_text = """ 
"""

template_gen_prompt_a_text = """ 
"""

template_gen_prompt_b_text = """ 
"""

template_sanitize_learning_objectives_text = """ 
"""

XML_templates= [
"""
<example>
    <exercise>
        <prompt>
            <type>Stelling</type>
            <text></text>
        </prompt>
        
        <options>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </options>
        
        <correct_answer></correct_answer>
    </exercise>

    <double_negative>
        -
        -
        
    </double_negative>
</example>
"""
    ,
"""
<example>
    <exercise>
        <prompt>
            <type>Vraag</type>
            <text></text>
        </prompt>
        
        <options>
            1. 
            2. 
            3.
            4.
        </options>
        
        <correct_answer></correct_answer>
    </exercise>

    <double_negative>
        -
        -
        
    </double_negative>
</example>
"""
    ,
"""
"""
]