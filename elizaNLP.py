# NOTE: refer to the README.md for the instructions on how to install the spaCy library

import spacy

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# List of fruits for the game
fruits = [
    "apple", "banana", "cherry", "grape", "orange", "mango", "lemon",
    "pineapple", "strawberry", "blueberry", "raspberry", "kiwi",
    "watermelon", "melon", "blackberry", "pear", "peach", "plum",
    "fig", "pomegranate", "coconut", "lime", "apricot", "dragon fruit",
    "nectarine", "guava", "lychee", "tangerine", "passion fruit"
]

fruit_descriptions = {
    "apple": ["sweet", "tart", "sour", "crisp", "green", "red", "medium", "round", "stem", "seeds"],
    "mango": ["sweet", "soft", "tropical", "yellow", "medium", "orange", "red", "green", "round", "stem"],
    "banana": ["sweet", "creamy", "yellow", "green", "medium", "long", "curved", "peel", "bunch", "tropical"],
    "blueberry": ["sweet", "tart", "small", "blue", "berry"],
    "blackberry": ["sweet", "tart", "small", "black", "blue", "berry", "thorns"],
    "raspberry": ["sweet", "fuzzy", "small", "red", "thorns"],
    "strawberry": ["sweet", "tart", "small", "red", "pink", "seeds", "stem"],
    "cherry": ["sweet", "tart", "small", "red", "seeds", "stem", "bunch","round"],
    "grape": ["sweet", "crisp", "small", "seedless", "purple", "green", "bunch", "round"],
    "watermelon": ["sweet", "crisp", "refreshing", "big", "red", "green", "a rind", "seeds", "round", "melon"],
    "honeydew melon": ["sweet", "soft", "refreshing", "big", "green", "a rind", "seeds", "round", "melon"],
    "cantaloupe": ["sweet", "soft", "refreshing", "big", "orange", "a rind", "seeds", "round", "melon"],
    "pear": ["sweet", "tart", "soft", "medium", "green", "yellow", "stem", "seeds", "round"],
    "plum": ["sweet", "tart", "soft", "medium", "purple", "a pit", "round"],
    "apricot": ["sweet", "soft", "medium", "fuzzy", "orange", "a pit", "round"],
    "peach": ["sweet", "soft", "medium", "fuzzy", "pink", "orange", "a pit", "round"],
    "kiwi": ["sweet", "tropical", "fuzzy", "refreshing", "green", "brown", "seeds", "round"],
    "pomegranate": ["sweet", "tart", "tropical", "medium", "red", "pink", "seeds", "round"],
    "pineapple": ["sweet", "tart", "tropical", "refreshing", "seedless", "spiky", "big", "yellow"],
    "orange": ["sweet", "tart", "sour", "citrus", "medium", "orange", "round", "stem", "seeds"],
    "grapefruit": ["sour", "tart", "citrus", "medium", "orange", "pink", "round", "stem", "seeds"],
    "lemon": ["sour", "tart", "citrus", "medium", "refreshing", "yellow", "round", "seeds"],
    "lime": ["sour", "tart", "citrus", "medium", "refreshing", "green", "round", "seeds"],
    "dragon fruit": ["sweet", "tropical", "seeds", "spiky", "medium", "pink", "green", "white"]
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
    negative = any(token.lemma_ in ["no", "negative", "nay", "nope", "nah", "no way", "not", "never", "nix", "uh-uh", "nope", "not at all", "absolutely not", "by no means", "not a chance", "decline", "refuse", "reject", "deny", "veto", "rebuff", "renounce", "repudiate", "retract", "revoke", "withdraw", "non", "none", "nothing", "nowhere", "neither", "null", "void", "zero"] for token in doc)
    unsure = any(token.lemma_ in ["unsure", "maybe", "perhaps", "possibly", "probably", "doubtful", "dubious", "questionable", "uncertain", "undecided", "undetermined", "don't know", "dont know", "idk"] for token in doc)

    return affirmative, negative, unsure

def guess_fruit():
    possible_fruits = list(fruit_descriptions.keys())
    while len(possible_fruits) > 1:
        clue = input("Describe the fruit or answer the question: ")
        doc = nlp(clue)
        keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

        # Filter possible fruits based on the clue/description
        possible_fruits = [fruit for fruit in possible_fruits if any(keyword in fruit_descriptions[fruit] for keyword in keywords)]

    while len(possible_fruits) > 1 and descriptors:
        descriptor = random.choice(descriptors)
        descriptors.remove(descriptor)

        # Determine if the descriptor is a noun or an adjective
        doc = nlp(descriptor)
        pos = doc[0].pos_  # Assuming the descriptor is a single word

        question = ""
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
        affirmative, negative, unsure = analyze_response(response)

        if affirmative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor in fruit_descriptions[fruit]]
        elif negative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor not in fruit_descriptions[fruit]]
        elif unsure:
            print("> Ok, let's try another one.")

    return f"> Is it a {possible_fruits[0]}?" if possible_fruits else "> I couldn't guess the fruit."

# Start the game
fruit_guess = guess_fruit()
print(fruit_guess)

# Analyze the user's response
response = input().strip().lower()
affirmative, negative, unsure = analyze_response(response)

# Check the user's response
if affirmative:
    print("> Yay! Thank you for playing.")
elif negative:
    print("Oh well. Good game!")
elif unsure:
    print("Let's try another one.")