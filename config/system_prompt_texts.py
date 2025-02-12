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
<task_definition>
   You assess multiple-choice exercise distractors (incorrect answer options) of a given exercise, to identify any distractors that are completely ineffective due to being too obviously wrong. Your final goal is to state your assessment of whether the exercise as a whole is acceptable or not. 
</task_definition>

<key_concepts>
    <effectiveness_criterion>
        A distractor is considered effective if it sounds plausible to at least some students. It's acceptable if most students would dismiss it, as long as not all of them would.
        The given exercise is acceptable only if ALL of its distractors are considered effective . 
    </effectiveness_criterion>
    
    <failure_threshold>
        A distractor fails when it would be dismissed even by a Dumb Student who:
        - Didn't prepare for the test at all
        - Has minimal domain knowledge
        - Has below average world knowledge
        - Is pretty stupid in general
    </failure_threshold>
</key_concepts>

<analysis_guidance>
    Your analysis should engage deeply with understanding the student perspective in the context of this particular exercise. Really try to vividly imagine the hypothetical Dumb Student, in line with the test's likely target demographic. They are bottom of their class. What would be their likely interpretations, their thought patterns? Really inhabit this perspective as you carefully examine each distractor one by one.
    
    Explore multiple angles in your reasoning. Consider edge cases, alternative interpretations, and different ways different students might approach the exercise. Take the exact phrasing of the exercise seriously. Document your thought process thoroughly, showing the nuance in your considerations.
</analysis_guidance>

<output_requirements>
    1. Focus solely on diagnosing the issue for the given distractors (no need to suggest improvements)
    2. Show detailed reasoning throughout your analysis
    3. Maintain nuance and depth in your exploration
    4. Finally (and only then, in your very last sentence) conclude with a clear, binary verdict about your diagnosis 
</output_requirements> 
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
# Learning Objective Extraction Task

Your task is to analyze a study text and extract high-quality learning objectives that will later serve as the basis for multiple-choice questions. Each learning objective must perfectly adhere to all specified requirements.

## Analysis Approach
Before extracting learning objectives:
* Carefully analyze the text's language level and target audience
* Note the terminology, voice (active/passive), and perspective (2nd/3rd person)
* Pay attention to the complexity of vocabulary and sentence structures used

## Core Requirements for Learning Objectives

### Format and Language
* Begin with "- The student knows that" (or equivalent in the text's language)
* Mirror the source text's:
  - Language level and vocabulary
  - Terminology and jargon
  - Voice (active/passive)
  - Perspective (2nd/3rd person)
  
<examples>
    <language_level_examples>
        <text>
            # Observeren Oefenen
            Dagelijks oefen je om zo objectief (zonder je eigen mening) mogelijk te observeren. Dit betekent onder andere dat je aan een zorgvrager vraagt of het klopt wat je hebt geobserveerd.
        </text>
        <too_difficult>
            - De student weet dat objectief observeren betekent dat de observatie zonder eigen mening plaatsvindt.
            - De student weet dat je dagelijks oefent om zo objectief mogelijk te observeren.
            - De student weet dat een zorgverlener de juistheid van observaties moet verifiëren bij de zorgvrager zelf.  
        </too_difficult>
        <explanation>The text's language is simple, showing that it was written for a simple target audience. Therefore, don't use any words that they might find difficult to understand (like "plaatsvinden" and "verifiëren"). Also, don't use the third person ("een zorgverlener") when the text uses second person.</explanation>
        <better>
            - De student weet dat objectief observeren betekent dat je zonder je eigen mening observeert.
            - De student weet dat je dagelijks oefent om zo objectief (zonder je eigen mening) mogelijk te observeren.  
            - De student weet dat je aan de zorgvrager vraagt of jouw observatie klopt.
        </better>
        <explanation>Now they are stated mirroring the language of the text, without introducing new, potentially difficult words.</explanation>
    </language_level_examples>
</examples>

### Content Quality
* **Falsifiable**: Must be unambiguously, demonstrably true or false
* **Factually Equivalent**: Represent exactly the knowledge as written
* **Specific**: Express the smallest coherent, testable knowledge unit, instead of several things at once

<examples>
    <specificity_examples>
        <too_broad>- De student weet dat het hart uit vier holtes bestaat: twee boezems aan de bovenkant en twee kamers aan de onderkant.</too_broad>
        <explanation>Combines multiple knowledge elements that could be tested separately</explanation>
        <better>
            - De student weet dat het hart uit vier holtes bestaat.
            - De student weet dat het hart uit twee boezems en twee kamers bestaat.
            - De student weet dat de boezems van het hart aan de bovenkant zitten.
            - De student weet dat de kamers van het hart aan de onderkant zitten.
        </better>
        <explanation>Focuses on each specific, testable knowledge element individually</explanation>
    </specificity_examples>
</examples>

### Additional notes
* 

### Language Precision
* Avoid universal terms ("always", "never") unless 100% accurate, and there are in fact no exceptions
* Avoid vague modifiers ("can", "could", "might", "may"), because those make meaningless statements
* Replace subjective terms ("often", "sometimes", "many", "few") with specific comparisons
* Use "important" only when there is no other option to say something more meaningful ("X is important" doesn't say much)

## Quality Assurance Process
1. Extract all potential learning objectives
2. For each objective, verify it meets ALL requirements
3. Refine and potentially split objectives until each one is:
   - Maximally specific
   - Perfectly aligned with source text, mirroring difficulty level and terminology
   - Completely falsifiable
   - Properly phrased
4. Return final list in the same language as the source text
"""


"""
<examples>
    <language_level_examples>
        <text>
            # Observeren Oefenen
            Dagelijks oefen je om zo objectief (zonder je eigen mening) mogelijk te observeren. Dit betekent onder andere dat je aan een zorgvrager vraagt of het klopt wat je hebt geobserveerd.
        </text>
        <too_difficult>
            - De student weet dat objectief observeren betekent dat de observatie zonder eigen mening plaatsvindt.
            - De student weet dat je dagelijks oefent om zo objectief mogelijk te observeren.
            - De student weet dat een zorgverlener de juistheid van observaties moet verifiëren bij de zorgvrager zelf.  
        </too_difficult>
        <explanation>The text's language is simple, showing that it was written for a simple target audience. Therefore, don't use any words that they might find difficult to understand (like "plaatsvinden" and "verifiëren"). Also, don't use the third person ("een zorgverlener") when the text uses second person.</explanation>
        <better>
            - De student weet dat objectief observeren betekent dat je zonder je eigen mening observeert.
            - De student weet dat je dagelijks oefent om zo objectief (zonder je eigen mening) mogelijk te observeren.  
            - De student weet dat je aan de zorgvrager vraagt of jouw observatie klopt.
        </better>
        <explanation>Now they are stated mirroring the language of the text, without introducing new, potentially difficult words.</explanation>
    </language_level_examples>
</examples>

        
            
        <too_broad>- De student weet dat het hart uit vier holtes bestaat: twee boezems aan de bovenkant en twee kamers aan de onderkant.</too_broad>
        <explanation>Combines multiple knowledge elements that could be tested separately</explanation>
        <better>
        - De student weet dat het hart uit vier holtes bestaat.
        - De student weet dat het hart uit twee boezems en twee kamers bestaat.
        - De student weet dat de boezems van het hart aan de bovenkant zitten.
        - De student weet dat de kamers van het hart aan de onderkant zitten.
        </better>
        <explanation>Focuses on each specific, testable knowledge element individually</explanation>
    </specificity_examples>
</examples>
"""

"""
< unnecessary > < / unnecessary >
< explanation > < / explanation >
"""

"""
<examples_of_>
    <bad_example>
        <content>
            content
        </content>
        <explanation>
            explanation
        </explanation>
    </bad_example>
    
    <good_example>

            <explanation>
            
            </explanation>
    </good_example>
</examples_of_> 
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