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

# new prompt 1
template_gen_prompt_a_text = """
# Learning Objective Extraction Task

Your task is to analyze a study text and extract high-quality learning objectives that will later serve as the basis for multiple-choice questions. Each learning objective must perfectly adhere to all specified requirements. Here are some examples of various good learning objectives (without the texts they're based on) to familiarize you with the concept:
<examples>
    <various_good_learning_objectives>
        - De student weet dat eenzaamheid subjectief is.
        - De student weet dat erfelijkheid een van de hoofddingen is die je persoonlijkheid vormen (naast opvoeding, sociale omgeving en zelfbepaling).
        - De student weet dat sociale omgeving een van de hoofddingen is die je persoonlijkheid vormen (naast erfelijkheid, opvoeding en zelfbepaling).
        - De student weet dat de secondary survey plaatsvindt wanneer de primary survey inclusief resuscitatie is afgerond.
        - De student weet dat de S in SBAR staat voor Situation ('situatie').
        - De student weet dat de B in SBAR staat voor Background ('achtergrond').
    </various_good_learning_objectives>
<examples>

## Analysis Approach
Before extracting learning objectives from the text:
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
            - De student weet dat als je iets observeert, je aan de zorgvrager vraagt of jouw observatie klopt.
        </better>
        <explanation>Now they are stated mirroring the language of the text, without introducing new, potentially difficult words.</explanation>
    </language_level_examples>
</examples>

### Content Quality
* **Self-contained**: Must be understandable without relying on any outside context, like 'previous' learning objectives (they will in fact be presented to the student non-chronologically, so they cannot build on each other) 
* **Falsifiable**: Must be unambiguously, demonstrably true or false 
* **Factually Equivalent**: Must represent exactly the knowledge as written
* **Specific**: Must express the smallest testable knowledge unit, instead of combining several at once. For knowledge that consists of parts, just focus on each part one by one (one learning objective focused on each), including callbacks to the whole. 

<examples>
    <self-contained_example>
        <too_context_dependent>- De student weet dat als je dit gevoel krijgt, je hierop moet letten en moet onderzoeken waar het vandaan komt.</too_context_dependent>
        <explanation>From just reading the learning objective, it is not clear what "dit" refers to</explanation>
        <better>- De student weet dat als je een onderbuikgevoel krijgt, je hierop moet letten en moet onderzoeken waar het vandaan komt.</better>
        <explanation>Now it includes the relevant part of the text such that the objective becomes self-contained, not referencing any info outside of it</explanation>
    </self-contained_example>
    <specificity_examples>
        <too_broad>- De student weet dat het hart uit vier holtes bestaat: twee boezems aan de bovenkant en twee kamers aan de onderkant.</too_broad>
        <explanation>Combines multiple knowledge elements that could be tested separately</explanation>
        <better>
            - De student weet dat het hart uit vier holtes bestaat (twee boezems aan de bovenkant en twee kamers aan de onderkant).
            - De student weet dat het hart uit twee boezems en twee kamers bestaat (samen vormen zij de vier holtes van het hart).
            - De student weet dat de boezems van het hart aan de bovenkant zitten (de twee kamers zitten aan de onderkant).
            - De student weet dat de kamers van het hart aan de onderkant zitten (de twee boezems zitten aan de bovenkant).
        </better>
        <explanation>Focuses on each smallest specific knowledge element individually, while maintaining coherence via the callback to the whole between brackets</explanation>
        <too_broad>- De student weet dat de Wvggz vier hoofddoelstellingen heeft: (1) het beperken of voorkomen van dwang, (2) het versterken van de rechtspositie van zorgvragers met een psychische aandoening, (3) het verbeteren van de kwaliteit van de zorg en (4) het leveren van (dwang)zorg op maat.</too_broad>
        <explanation>'Knowing Wggz's key objectives' can be seen as one coherent learning objective, but it consists of too many clearly discrete parts that each can (and therefore should) be tested separately.</explanation>
        <better>
            - De student weet dat "dwang beperken" een van de vier hoofddoelen is van de Wvggz (naast het versterken van de rechtspositie van zorgvragers met een psychische aandoening, verbeteren van de kwaliteit van de zorg en (dwang)zorg op maat leveren.
            - De student weet dat "het versterken van de rechtspositie van zorgvragers met een psychische aandoening" een van de vier hoofddoelen is van de Wvggz (naast het beperken of voorkomen van dwang, het verbeteren van de kwaliteit van de zorg en het leveren van (dwang)zorg op maat).
            - De student weet dat "het verbeteren van de kwaliteit van de zorg" een van de hoofddoelen is van de Wvggz (naast het beperken of voorkomen van dwang, het versterken van de rechtspositie van zorgvragers met een psychische aandoening en het leveren van (dwang)zorg op maat).
            - De student weet dat "het leveren van (dwang)zorg op maat" een van de hoofddoelen is van de Wvggz (naast het beperken of voorkomen van dwang, het versterken van de rechtspositie van zorgvragers met een psychische aandoening en het verbeteren van de kwaliteit van de zorg).
        </better>
        <explanation>This repetition may seem tedious, but it is crucial for composite knowledge like this. It allows us to later craft effective, self-contained multiple choice questions based on each knowledge part independently, while retaining the connection to the whole. This way, we can do targeted, piecemeal testing of the student's knowledge without sacrificing coherence.</explanation>
    </specificity_examples>
</examples>

### Additional notes
* If a term is explained in the text, and it's central to the topic, knowing what it means should also become a learning objective
* If a term is explained in the text, also explain it briefly (between parentheses) in each learning objective that uses it 
* If the text is so knowledge dense that it contains more than 16 potential learning objectives, cap them at around that number and eliminate the less important ones. For non-hierarchical learning objectives (all equally important), just trim randomly
* Exclude examples, they are not important knowledge (unless they are critical to understanding the topic OR there would otherwise be less than 3 learning objectives)


### Language Precision
* Avoid universal terms ("always", "never") unless 100% accurate, and there are in fact no exceptions
* Avoid vague modifiers ("can", "could", "might", "may"), because those make meaningless statements
* Replace subjective terms ("often", "sometimes", "many", "few") with specific comparisons
* Use "important" only when there is no other option to say something more meaningful ("X is important" doesn't say much)

## Quality Assurance Process
1. Extract all potential learning objectives (up to ~16 max)
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
        <explanation>Now they are stated mirroring the language of the text, without introducing new, potentially difficult words. Words that are explained in the text, need to be explained in each learning objective that reuses it between parentheses as well.</explanation>
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

# existing old (current) prompt stripped refocused for LOs only
template_gen_prompt_b_text = """
You are given a study text. Based on this, you will identify learning objectives. Follow the following protocol meticulously:

# Protocol for Creating Exercises for eLearning Modules
## General Working Method

### Text Orientation  
Assigned a study text, your initial task is to read it to understand the topic for creating exercises.

### Learning objectives 
Based on the text, define clear, concise learning objectives. Make sure you have enough learning objectives so that all information is covered, but not too many so that learning objectives won't overlap.  It's really important that every learning objective only states 1 single fact and doesn't combine multiple facts. Choose objectives based on text analysis and audience level. Objectives always start with 'The student knows that', or whichever semantic equivalent matching the language of the study text (eg. for Dutch texts, use 'De student weet dat'). 

Observe the following rules meticulously when writing learning objectives:

#### Avoid 'always' and 'never' 
Don't use words like 'always' or 'never' in learning objectives, it is likely an exception exists. Instead use constructions like 'X *fits with* Y', 'X *suggests* Y', 'X *is more common than* Y'

So not:
> BAD: The students knows that fever *never* occurs with a viral infection. 
> BAD: The students knows that fever *always* occurs with a viral infection. 

But:
> GOOD: The students knows that fever is a symptom *that fits with* a viral infection. 

#### Avoid 'can', 'could', 'may' or 'might' 
Don't use words like *'can'*, *'could'*, *'may'* or *'might'* in learning objectives, because almost everything can, could or might be something, so too suggestive. Instead use constructions like 'X *fits with* Y', 'X *suggests* Y', 'X *is more common than* Y'

So not:
> BAD: The students knows that pain *might* occur with rheumatoid arthritis.
> BAD: The students knows that pain *can* occur with rheumatoid arthritis.
> BAD: The students knows that pain *could* occur with rheumatoid arthritis.
> BAD: The students knows that pain *may* occur with rheumatoid arthritis.

But: 
> GOOD: The students knows that pain *is a symptom of* rheumatoid arthritis.

#### Avoid subjective terminology like many, few and common 
Don't use words like *'many'*, *'few'*, *'common'*, *'rare'* et cetera as these are subjective. Instead be specific. Instead use terminology like *'in most cases'* or compare: *'symptom A is more common than symptom B'*. 

Example of a bad learning objective, leading to suggestive or subjective answers: 
> BAD: The student knows that fever commonly occurs with a viral infection. 

#### Avoid important, essential significant
Don't use words like *'important'*, *'essential'*, *'significant'* et cetera in learning objectives, as these are prone to subjectivity. 

Examples of a bad learning objective, leading to suggestive or subjective answers: 
> BAD: The students knows that it's *important* to rest when having a viral infection. 

The objective uses the word *'important'* which is subjective.  

> BAD: The students knows that it's *essential* to rest when having a viral infection. 

The objective uses the word *'essential'* which is subjective. 

> BAD: The students knows that fever has a *significant* effect on how people feel when they are sick. 

The objective uses the word *'significant'* which is subjective. 

> BAD: The student knows that drinking *enough* water is *important* to stay hydrated. 

The objective uses the word *'important'* which is subjective. Also the word *'enough'* is subjective. 


A good example is: 

> GOOD: The student knows that proteinuria is a symptom of nephrotic syndrome. 

An example of a bad learning objective: 

> BAD: The student knows the symptoms of nephrotic syndrome. 

The bad objective does not specify a single fact as symptoms are not specified.

A good example is:

>  GOOD: The student knows that besides pain, rheumatoid arthritis also causes loss of mobility. 

An example of a bad learning objective:

> BAD: The student knows that problems with movement due to joint problems, such as rheumatism, can be painful or completely limit movement

The latter objective does not specify a single fact but combines two (can be painful or completely limit movement). The first objective focuses on the 'loss of mobility' element, while the 'pain- element' is already considered known. The exercises generated by this learning objective will test the 'loss of mobility' element (so not the 'pain-element' 
"""

template_sanitize_learning_objectives_text = """
"""

template_write_fluster_a_text= """
# Task outline

Given a learning objective, your goal is to write an exercise set of 3 high-quality multiple choice exercises that all test the exact same key fact that's stated in the learning objective.


# Concepts

## Learning objective
A learning objective states a specific fact. For example: "De student weet dat de Wet Bopz sinds 1994 in gebruik was (tot hij in 2020 werd opgevolgd door de Wvggz)." It consist of the fact of focus, and sometimes some additional context between parentheses.

## Exercise
An exercise tests the fact that is stated in the learning objective. It consists of:
1. A prompt, posing to the student:
    - A question or statement
    - (Optional) Theory, additional information to clarify the question or statement
2. Choices, which are the multiple answer options that are presented to the student as potential answers to the prompt.
3. Correct answer, which indicates which of the choices is the correct answer to the prompt.
4. (Optional) Explanation, explaining or expanding on the answer to the student to facilitate increased learning. 
The student is always first presented with 1 and 2 (prompt and choices), and then, after they've picked an answer, they get to see 3 and 4 (the correct answer and optionally an explanation).    

## Exercise set
An exercise set comprises 3 exercises that all test the same single learning objective in three different ways: one bigger multiple choice exercise and two smaller true/false statements.

## Distractors
Distractors are the alternative answer option choices of the exercises that are not the correct answer. The false statement can also be considered a distractor (tempting the student to thing it is correct). Distractors are in fact the most important part of the exercises, because they often either make or break it. This is because distractors are difficult to get right, because in order to be effective they need to strike a precarious balance between "plausible-sounding" and yet "not too close to the truth", both at the same time. More on that in the requirements section.

## Theory (optional)
Theory is sometimes shown before answering the exercise, as an optional part of the prompt to clarify the question.

## Explanation (optional)
An explanation should sometimes be presented to the student after they've answered the exercise, as an optional part of the correct answer reveal to better facilitate learning.  


# Examples

## Exercise set for the learning objective: "De student weet dat de Wet Bopz sinds 1994 in gebruik was (tot hij in 2020 werd opgevolgd door de Wvggz)".
<exercise_set>
    <multiple_choice_exercise>
        <prompt>
            Stelling:
            De wet Bopz was sinds ..... in gebruik.
        </prompt>
        
        <choices>
            1. 1984
            2. 1999
            3. 2004
            4. 2009
        </choices>
        <correct_answer>2</correct_answer>
        <explanation>In 2020 werd de wet Bopz opgevolgd door de Wvggz.</explanation>
    </multiple_choice_exercise>
    
    <true_statement>
        <prompt>
            Stelling:
            De wet Bopz was sinds 1994 in gebruik.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>1</correct_answer>
        <explanation>In 2020 werd de wet Bopz opgevolgd door de Wvggz.</explanation>
    </true_statement>

    <false_statement>
        <prompt>
            Stelling:
            De wet Bopz was sinds 1984 in gebruik.
        </prompt>
        
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>2</correct_answer>
        <explanation>De wet Bopz was sinds **1994** in gebruik. Tot 2020, toen hij werd opgevolgd door de Wvggz.</explanation>
    </false_statement>
</exercise_set>

## Exercise set for the learning objective: "De student weet dat je dagelijks oefent om zo objectief (zonder je eigen mening) mogelijk te observeren."
<exercise_set>
    <multiple_choice_exercise>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Vraag:
            Wat moet je doen om zo objectief mogelijk te observeren?
        </prompt>
        
        <choices>
            1. Je intuïtie volgen
            2. Veel theorie leren
            3. Iemand anders erbij roepen
            4. Dagelijks oefenen
        </choices>
        <correct_answer>4</correct_answer>
    </multiple_choice_exercise>
    
    <true_statement>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Stelling:
            Om zo objectief mogelijk te observeren moet je dagelijks oefenen.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>1</correct_answer>
    </true_statement>

    <false_statement>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Stelling:
            Om zo objectief mogelijk te observeren moet je een keer per jaar oefenen.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>2</correct_answer>
        <explanation>Om zo objectief mogelijk te kunnen observeren, is het belangrijk om regelmatig, bij voorkeur <b>dagelijks</b>, te oefenen.</explanation>
    </false_statement>
</exercise_set>


# Requirements

## Exercise
Each of the 3 exercises must test the very same key fact in the given learning objective (the info that's not in parentheses). Assume this described fact is self-evident, not in need of any further outside sourcing or substantiation. Any text between parentheses must only be used in the Theory or Explanation sections of the exercises.

## Prompt
The information in the prompt should only contain information that's also present in the learning objective. Don't reference anything outside of it, nor itself. Simply pose the ideal question or statement to test the student's knowledge of the described fact.

## Theory & Explanation (optional)
Theory or Explanation should only be added to all 3 exercises if there's additional info present in the learning objective (often between parentheses, or as a subclause) that is outside of the main fact that's to be tested.
### Theory (optional)
Put any info here that is useful for the student to know before answering the question, as context to clarify the question or statement. The student is prompted with this together with the posing of the rest of the exercise.
### Explanation (optional)
Put any info there that is not necessary to clarify the prompt beforehand (or that might in fact spoil the answer). The explanation section is for supplemental info that'll help the student to facilitate learning after they've already seen the correct answer. Usually no explanation is needed. The false statement however, always needs an explanation, to tell the student why the statement is incorrect (explaining what the true statement would have been).

## Distractors
A good distractor makes a student pause and consider it, separating those who understand the material from those who do not. A bad distractor fails to do this; it can either:
1. Confuse or trick even well-prepared students into believing it might be correct (“too close to the truth”)
2. Be so obviously wrong that no one would reasonably choose it, not even the least knowledgeable student (“too obviously false”).
To be effective, distractors must therefore look "very plausible to someone who doesn't know the topic" and yet remai n "clearly wrong to someone who knows the topic well", all at the same time.
Distractors are too close to the truth, when they are so similar to the correct answer that experts might debate whether they're also valid. They create unnecessary ambiguity and frustrate knowledgeable test-takers, for example by containing partial truths.
Distractors are too obviously false, when they are clearly ridiculous or fantastical to even the dumbest student.
The ideal distractor falls in the middle of this spectrum - plausible enough to tempt those with incomplete knowledge, but clearly incorrect to those who understand the material.

## Language level
Try to exactly match the terminology and language difficulty level from the learning objective. If it's stated in simple words, use equally simple words in the exercises as well.

## Output format
Output format doesn't matter. Only prioritize thorough reasoning to arrive at high-quality exercises that satisfy all of the above requirements.

# Approach

Think long and hard about the ideal three exercises to test the given learning objective. Especially spend a lot of time iteratively coming up with good distractors and a good "false statement", to make sure they optimally satisfy the distractors requirements.
As intuition pumps:
- To guard against picking distractors that are too obviously false: Really try to imagine a relatively dumb student among the target audience for the specific given learning objective. Would they feasible find each distractor at least somewhat plausible?
- To guard against picking distractors that are too close to the truth: Try to imagine a panel of experts judging the distractors. All of them should agree that the correct answer is clearly the best answer for this exercise, and none of them should doubt that any other choices would also be kinda correct. 
If you're unsure about any of your distractors or "false statements" one way or the other, adapt them accordingly, and run the thought experiment again, until you get all distractors just right.
After lots of iterative prep, trying out different things and reasoning through a wide range of potential options, finally return a complete exercise set of 1 bigger multiple choice exercise and 2 smaller True/False statements.   
"""

uitgangspunt_template_for_writing_a_fluster = """
# Task outline
Given a learning objective, your goal is to write an exercise set of 3 high-quality multiple choice exercises that all test the exact same knowledge that's stated in the learning objective.

# Concepts
## Learning objective
Tests a specific fact. For example: "De student weet dat de Wet Bopz sinds 1994 in gebruik was (tot hij in 2020 werd opgevolgd door de Wvggz)."
All exercises must test the very same specific key part of the given learning objective, focusing only on info that's not in parentheses. Any text between parentheses must only be used in the Theory or Explanation sections of the exercises (Theory if it's important for understanding the exercise beforehand, explanation if it's .

## Exercise set
Comprises 3 exercises that all test the same single learning objective: one bigger multiple choice exercise and two smaller true/false statements. See this example:
<exercise_set>
    <multiple_choice_exercise>
        <prompt>
            Stelling:
            De wet Bopz was sinds ..... in gebruik.
        </prompt>
        
        <choices>
            1. 1984
            2. 1999
            3. 2004
            4. 2009
        </choices>
        <correct_answer>2</correct_answer>
        <explanation>In 2020 werd de wet Bopz opgevolgd door de Wvggz.</explanation>
    </multiple_choice_exercise>
    
    <true_statement>
        <prompt>
            Stelling:
            De wet Bopz was sinds 1994 in gebruik.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>1</correct_answer>
        <explanation>In 2020 werd de wet Bopz opgevolgd door de Wvggz.</explanation>
    </true_statement>

    <false_statement>
        <prompt>
            Stelling:
            De wet Bopz was sinds 1984 in gebruik.
        </prompt>
        
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>2</correct_answer>
          <explanation>De wet Bopz was sinds **1994** in gebruik. Tot 2020, toen hij werd opgevolgd door de Wvggz.</explanation>
    </false_statement>
</exercise_set>

Here's another example of an exercise set, this time for the learning objective: "De student weet dat je dagelijks oefent om zo objectief (zonder je eigen mening) mogelijk te observeren."
<exercise_set>
    <multiple_choice_exercise>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Vraag:
            Wat moet je doen om zo objectief mogelijk te observeren?
        </prompt>
        
        <choices>
            1. Je intuïtie volgen
            2. Veel theorie leren
            3. Iemand anders erbij roepen
            4. Dagelijks oefenen
        </choices>
        <correct_answer>4</correct_answer>
    </multiple_choice_exercise>
    
    <true_statement>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Stelling:
            Om zo objectief mogelijk te observeren moet je dagelijks oefenen.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>1</correct_answer>
    </true_statement>

    <false_statement>
        <prompt>
            Theorie:
            Objectief betekent "zonder je eigen mening".
            
            Stelling:
            Om zo objectief mogelijk te observeren moet je een keer per jaar oefenen.
        </prompt>
    
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>2</correct_answer>
        <explanation>Om zo objectief mogelijk te kunnen observeren, is het belangrijk om regelmatig, bij voorkeur <b>dagelijks</b>, te oefenen.</explanation>
    </false_statement>
</exercise_set>


## Distractors
The alternative answer options of the multiple choice exercise that are not the correct answer are called distractors. These are the most important part of the exercise. Effective distractors strike an optimal balance between "very plausible to someone who doesn't know the answer to the question" and "clearly wrong to someone who does know the answer to the question".

## Theory 
Optional. Sometimes there's additional knowledge present in the learning objective (often between parentheses) that is not the direct focus to test, but useful to know for the student beforehand to better understand the question. This is then added as Theory in the prompt. The student gets to see this as part of the exercise prompt.

## Explanation
Optional. Sometimes there's additional knowledge present in the learning objective (often between parentheses, or as a subclause) that is not the direct focus to know, nor is it necessary to clarify the prompt. If this is useful related, additional info, add it to the explanation, so that the student gets to see this after they pick their answer. The false statement always needs an explanation, to tell the student why the statement is incorrect (explaining what the true statement would have been). Other exercises should only get an explanation if the learning objective contains appropriate info for this. 

# Approach
Think long and hard about the ideal three exercises to test the given learning objective. Especially spend a lot of time picking good distractors for the first multiple choice exercise. 
Imagine the typical slightly more stupid target student among the target audience for this learning objective. Would they sometimes find each distractor sound appealing if they hadn't studied for the test? We want to avoid the possibility that they can too easily dismiss and eliminate a distractor as clearly not a serious option, just on the basis of it looking weird to them. Imagine whether very stupid students with limited general knowledge, and no knowledge of the topic of the exercise, might find the distractor plausible. That's the goal. 
At the same time, a distractor must not be too close to the truth either. That would be misleading. Imagine asking 10 domain experts to judge this. All of them should agree that the correct answer is the clearly best answer in this exercise. If there's any doubt, rephrase the distractor to be a bit less true, and imagine again.
After lots of iterative prep and reasoning, considering a wide range of options, weighing what would be the best, finally return a complete exercise set of 1 multiple choice exercise and 2 statements.
 
## Pointers
- Try to exactly match the content and language level in the learning objective. If it's stated in simple words, use equally simple words in the exercises as well.
- Output format doesn't matter: prioritize careful reasoning.
"""






"""
<multiple_choice_exercise>
    <prompt>
    
    </prompt>
    
    <choices>
    
    </choices>
    <correct_answer></correct_answer>
    <explanation></explanation>
</multiple_choice_exercise>

<true_statement>
        <prompt>
            
        </prompt>

        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>1</correct_answer>
        <explanation></explanation>
</true_statement>
<false_statement>
        <prompt>

        </prompt>
        <choices>
            1. Deze stelling is correct
            2. Deze stelling is niet correct
        </choices> 
        <correct_answer>2</correct_answer>
        <explanation></explanation>
</false_statement>

"""

# The existing prompt in Course Generator webapp
template_write_fluster_b_text = """
You are given a learning objective. Based on this, you will create an exercise set of 3 exercises. 
Follow the following protocol meticulously:

# Protocol for Creating Exercises for eLearning Modules
## Definitions:
### Exercise
An exercise assesses knowledge related to a specific learning objective.

### Exercise set
An exercise set, comprising three exercises, tests the same learning objective and combines various exercise types targeting that objective.

## General Working Method

### Exercise Structure  
Below is the recommended exercise structure. Headings in brackets are optional.

#### Exercise sets
Create an exercise set for each objective. Make sure all exercises in the set test the given learning objective only and do not (partially) test anything else. Consequently, all exercises in the set test the same learning objective.
Also make sure that the exercise types vary. 

#### (Theory:/Case:)  
An exercise might begin with 'theory' for context or a 'case', a practical scenario, followed by a related exercise.

Example:
> Case:   A 23 year old woman presents at the ED due to exacerbation of
> bronchial asthma. She was cyanotic and can only speak in short
> sentences. ABG measurement showed the following values:     
> **pH:** 7.40  
> **PaCO2:** 40 mmHg/5.3 kPa  
> **HCO3:** 24 mmol/L  
> Question: What is the patient's acid-base abnormality?

#### Question/Statement:  
Ensure questions or statements are concise. End questions with a question mark and statements with a period. Write the question or statement in a JSON property called *'question'*

#### Multiple-Choice Answers  
Formulate answer choices briefly. Start with a capital letter. List answers without labels like A) B) C) or 1. 2. 3. List the correct answer choice in the JSON property *'answer'* and the remaining answer choices in a JSON array of strings called *'distractors'*

#### (Extra Info:)  
Provide additional information after each exercise for clarification, especially when the correct answer isn't obvious from the question. If it is just a repeat of the question and/or answer without adding anything for clarity, leave the extra info out. Write the extra info in the optional JSON property *'explanation'*.

### Exercise set
#### Variants in a exercise set
Create for every learning objective a exercise set consisting of three variants: 
- Question or fill in the blank with 3 or 4 answers choices  
- Correct/incorrect statement, answer is correct  
- Correct/incorrect statement, answer is incorrect  

Creating variants prevents students from just recognizing the exercise and answer, and encourages thinking about the correct answer.

#### Multiple choice question (mcq)
Label a mcq with 'question' and end with a question mark. Example:  

    [
    	{{
    		'question': 'Question: Which layer of the digestive tract has the myenteric neural plexus?',
    		 'answer': 'Muscular layer'
    		 'distractors': [
    			 'Mucosa',
    			 'Submucosa',
    			 'Serosa'
    		 ]
    	 }}
    ]

#### Multiple choice statement (mcs)
Create a statement with a fill in the blank. Use 'statement' instead of 'question' and end with a full stop. Use exactly 5 dots for the gap.  Never have more than 1 gap. Example:  
```json
    [
    	{{
    		'question': 'Statement: The ..... is the inner lining of the digestive tract. ',
    		 'answer': 'Mucosa',
    		 'distractors': [
    			 'Muscular layer',
    			 'Submucosa',
    			 'Serosa'
    		 ]
    	 }}
    ]
```
##### Correct/incorrect exercise set variants
Two variants in the exercise set, can be derived from the mcq or mcs. One has the correct mcq/mcs answer (answer “This statement is correct”), the other has an incorrect mcq/mcs answer (answer “This statement is incorrect”). Balance the correct and incorrect exercises in each exercise set. Start with a mcq or mcs followed by the 2 correct/incorrect variants.  


#### Avoid double negatives
Don't use negations like 'no' or 'not' or 'never' or words with a comparable meaning in the statement / question in order to avoid double negations with the 'incorrect' answer option.

#### Avoid 'always' and 'never' 
Don't use words like 'always' or 'never' in exercise statements or questions, it is likely an exception exists rendering the statement or question inherently incorrect.

So not:
> Statement: Fever can occur with a viral infection. 
> Question: What can occur with a viral infection. 

But:
> Statement: fever is a classic symptom of a viral infection. 
> Question: What is a classic symptom of a viral infection. 

#### Avoid 'can', 'could' or 'might' 
Don't use words like 'can', 'could' or 'might' in exercise statements or questions, because almost everything can, could or might be something, rendering the statement or question inherently correct.

So not:
> Statement: pain might occur with rheumatoid arthritis.
> Question: what symptoms can occur with rheumatoid arthritis?

But: 
> Statement: pain is a symptom that fits rheumatoid arthritis.
> Question: Which symptom best describes rheumatoid arthritis?

#### Using theory
Starting an exercise with Theory isn't mandatory. Add it for context or to shorten the question/statement.

#### Providing context
Each exercise should be clear on its own, also without the context of the study text it is about. Consider adding theory for clarity if needed. 

#### Shortening the statement/question
Keep statements/questions short and concise. Put extra context in the theory section.  

Example:  instead of
```json
    {{
    	'question': 'Statement: Between the liver and the anterior abdominal wall and diaphragm is the .....  ',
    	'answer': 'Falciform ligament ',
    	'distractors': {{'Greater omentum', 'Lesser omentum', 'Mesentery proper'}}
    }}
```
move some info to the theory for clarity:  
```json
    {{
    	'question': 'Theory: A visceral mesentery connects the liver to the anterior abdominal wall and diaphragm.\nQuestion: Which mesentery is this? ',
    	'answer': 'Falciform ligament ',
    	'distractors': {{'Greater omentum', 'Lesser omentum', 'Mesentery proper'}}
    }}
```
### Answer options  
#### Format and length  
Maintain similar format and length for all options in an exercise.

#### Choosing plausible incorrect options
Select incorrect options that might seem true to someone who doesn't know the answer.

#### Numbers
Use numbers only if relevant. For cut-off points, ensure incorrect answers are truly incorrect. Use terms like 'cut-off point' or 'lower/upper limit' for clarity.
For example:
```json
    {{
		"question": "Statement: A systolic blood pressure less than 70 mmHg is considered hypotension.",
		"answer": "This statement is incorrect",
		"distractors": [
	        "This statement is correct"
		],
		"explanation": "It is considered hypotension from 90 mmHg."
    }}
```    
The statement above is actually correct because less than 70 is also less than 90! What the writer intended to test was the cut-off point. You can solve this problem by explicitly using the terms 'cut-off point' or 'lower/upper limit' in the question


#### Accuracy 
Always aim to avoid debates over exercise accuracy. Correct answers must be wholly true, and incorrect ones entirely false, eliminating any argument possibility.  
Be precise. Shun absolute terms like 'never' or 'always', as they imply complete rightness or wrongness, which is rarely the case due to real-world exceptions. Choose words like 'typically', 'most characteristic of', or 'in most cases' and use relative terms such as “Is best described by ….”. When stating 'more/less than', clarify what it's in comparison to. Eschew 'can'. Including 'can' in questions or statements likely makes your wrong options not fully incorrect, as theoretically, much can occur.
"""


template_refine_fluster_text = """
Given some source data containing exercises, correct any spelling errors. 
"""


template_sanitize_fluster_text = """
Your task is to reformat the exercises, retaining all information. This should be your only output: a neat reformatted representation of all exercises. Instead of listing the index of the correct answer, show it by adding a little arrow indicator after the correct answer option, like this:

#. [answer option] ⬅️

Roughly follow the following template:

1. **Multiple-choice exercise**
[exercise 1]

2. **Correct statement**
[exercise 2]

3. **Incorrect statement**
[exercise 3]
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