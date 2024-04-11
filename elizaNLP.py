import spacy
import random

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

fruit_descriptions = {
    "apple": ["sweet", "tart", "sour", "crisp", "green", "red", "medium", "round", "stem", "seeds"],
    "mango": ["sweet", "soft", "tropical", "yellow", "medium", "orange", "red", "green", "round", "stem", "summer"],
    "banana": ["sweet", "creamy", "yellow", "green", "medium", "long", "curved", "peel", "bunch", "tropical"],
    "blueberry": ["sweet", "tart", "small", "blue", "berry", "summer"],
    "blackberry": ["sweet", "tart", "small", "black", "blue", "berry", "thorns", "summer"],
    "raspberry": ["sweet", "fuzzy", "small", "red", "thorns", "summer"],
    "strawberry": ["sweet", "tart", "small", "red", "pink", "seeds", "stem", "summer", "spring"],
    "cherry": ["sweet", "tart", "small", "red", "seeds", "stem", "bunch","round", "summer", "spring"],
    "grape": ["sweet", "crisp", "small", "seedless", "purple", "green", "bunch", "round", "summer", "fall"],
    "watermelon": ["sweet", "crisp", "refreshing", "big", "red", "green", "rind", "seeds", "round", "melon", "summer"],
    "honeydew melon": ["sweet", "soft", "refreshing", "big", "green", "rind", "seeds", "round", "melon", "summer"],
    "cantaloupe": ["sweet", "soft", "refreshing", "big", "orange", "rind", "seeds", "round", "melon", "summer"],
    "pear": ["sweet", "tart", "soft", "medium", "green", "yellow", "stem", "seeds", "round", "summer", "fall"],
    "plum": ["sweet", "tart", "soft", "medium", "purple", "pit", "round", "summer"],
    "apricot": ["sweet", "soft", "medium", "fuzzy", "orange", "pit", "round", "summer"],
    "peach": ["sweet", "soft", "medium", "fuzzy", "pink", "orange", "pit", "round", "summer", "spring"],
    "kiwi": ["sweet", "tropical", "fuzzy", "refreshing", "green", "brown", "seeds", "round", "fall", "winter"],
    "pomegranate": ["sweet", "tart", "tropical", "medium", "red", "pink", "seeds", "round", "fall"],
    "pineapple": ["sweet", "tart", "tropical", "refreshing", "seedless", "spiky", "big" "yellow"],
    "orange": ["sweet", "tart", "sour", "citrus", "medium", "orange", "round", "stem", "seeds", "winter"],
    "grapefruit": ["sour", "tart", "citrus", "medium", "orange", "pink", "round", "stem", "seeds", "winter"],
    "lemon": ["sour", "tart", "citrus", "medium", "refreshing", "yellow", "round", "seeds"],
    "lime": ["sour", "tart", "citrus", "medium", "refreshing", "green", "round", "seeds"],
    "dragon fruit": ["sweet", "tropical", "seeds", "spiky", "medium" "pink", "green", "white"]
}
# apple, mango, banana, blueberry, blackberry, raspberry, strawberry, cherry, grape, watermelon, honeydew melon, cantaloupe, pear, plum, apricot, peach, kiwi, pomegranate, pineapple, orange, grapefruit, lemon, lime, dragon fruit

def extract_descriptors(fruit_descriptions):
    descriptors = set()

    for description_list in fruit_descriptions.values():
        # Join the list of descriptions into a single string
        description = ' '.join(description_list)
        doc = nlp(description)

        for token in doc:
            if token.pos_ in ['NOUN', 'ADJ']:
                descriptors.add(token.lemma_)

    return list(descriptors)

def analyze_response(response):
    doc = nlp(response)
    
    affirmative = any(token.lemma_ in ["yes", "affirmative", "indeed", "absolutely", "certainly", "sure", "definitely", "of course", "yeah", "yep", "yup", "aye", "roger", "uh-huh", "right", "okay", "agreed", "true", "yea", "correct", "alright", "amen", "positively", "undoubtedly", "yah", "yass", "exactly", "naturally", "precisely", "assuredly", "aha", "agreed", "granted", "undoubtedly", "unquestionably", "yesh"] for token in doc)

    negative = any(token.lemma_ in ["no", "negative", "nay", "nope", "nah", "no way", "not", "never", "nix", "uh-uh", "nope", "not at all", "absolutely not", "by no means", "not a chance", "decline", "refuse", "reject", "deny", "veto", "rebuff", "renounce", "repudiate", "retract", "revoke", "withdraw", "non", "none", "nothing", "nowhere", 
    "neither", "null", "void", "zero"] for token in doc)

    unsure = any(token.lemma_ in ["unsure", "maybe", "perhaps", "possibly", "probably", "doubtful", "dubious", "questionable", "uncertain", "undecided", "undetermined", "don't know", "dont know", "idk"] for token in doc)

    return affirmative, negative, unsure

def guess_fruit():
    possible_fruits = list(fruit_descriptions.keys())
    descriptors = extract_descriptors(fruit_descriptions)
       # Additional questions
    questions = [
        "How does the fruit taste?",
        "Could you picture the size of the fruit? Is it small, medium, or large?",
        "When you think of the fruit, does it remind you of any specific season or environment in which it's typically found?",
        "When you envision the fruit, does it have any specific features like having seeds?",
        "In terms of its appearance, does the fruit have any unique shapes, such as round or long?",
        "Does it have any distinguishing factors such as having thorns, a stem, etc.?",
        "What family does the fruit belong to? E.g., melon, citrus.",
        "What color is the inside of the fruit?",
        "How is the texture of the fruit when you bite into it?"
        "What is the hardness of the fruit?"
    ]

    # First question to narrow down the possible fruits
    print("> Think of a fruit and I'll try to guess it! Describe your fruit: ")
    response = input().strip().lower()

    # Process the user's response to extract descriptors
    response_descriptors = extract_descriptors({'response': [response]})

    # Filter the possible fruits based on the user's response
    possible_fruits = [fruit for fruit in possible_fruits if any(descriptor in fruit_descriptions[fruit] for descriptor in response_descriptors)]

    while len(possible_fruits) > 1 and descriptors:
        descriptor = random.choice(descriptors)
        descriptors.remove(descriptor)

        # Determine if the descriptor is a noun or an adjective
        doc = nlp(descriptor)
        pos = doc[0].pos_  # Assuming the descriptor is a single word

        if pos == 'NOUN':
            print(f"The descriptor '{descriptor}' is a noun.")
            question = f"> Does the fruit you're thinking of {descriptor}?"
        elif pos == 'ADJ':
            print(f"The descriptor '{descriptor}' is an adjective.")
            question = f"> Is the fruit you're thinking of {descriptor}?"
        else:
            print(f"The descriptor '{descriptor}' is not a noun or an adjective.")

        print(question)
        response = input().strip().lower()
        affirmative, negative = analyze_response(response)

        if affirmative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor in fruit_descriptions[fruit]]
        elif negative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor not in fruit_descriptions[fruit]]
        else:
            print("> Ok, let's try another one.")

    return possible_fruits[0] if possible_fruits else "> I couldn't guess the fruit."

# Start the game
fruit_guess = guess_fruit()
print(f"> Is it a {fruit_guess}?")
