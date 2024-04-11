import spacy
import random

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

fruit_descriptions = {
    "apple": ["sweet", "sour", "crisp", "green", "red"],
    "mango": ["sweet", "soft", "tropical", "yellow", "orange", "red"],
    "banana": ["sweet", "creamy", "yellow", "long"],
    "blueberry": ["sweet", "small", "blue"],
    "blackberry": ["sweet", "small", "black", "blue"],
    "raspberry": ["sweet", "fuzzy", "small", "red"],
    "grape": ["sweet", "crisp", "small", "seedless", "purple", "green"],
    "watermelon": ["sweet", "crisp", "refreshing", "big", "red", "green", "pink"],
    "pear": ["sweet", "soft", "green"],
    "plum": ["sweet", "soft", "small", "purple"],
    "apricot": ["sweet", "soft", "fuzzy", "small", "orange"],
    "peach": ["sweet", "soft", "fuzzy", "pink", "orange"],
    "kiwi": ["sweet", "tropical", "fuzzy", "refreshing", "green"],
    "pineapple": ["sour", "tropical", "refreshing", "yellow"],
    "orange": ["sour", "citrusy", "orange", "round"],
    "lemon": ["sour", "citrusy", "refreshing", "yellow"],
    "lime": ["sour", "citrusy", "refreshing", "green"]
}

# Function to extract descriptors from fruit descriptions
def extract_descriptors(fruit_descriptions):
    descriptors = set()
    for description in fruit_descriptions.values():
        doc = nlp(description)
        for token in doc:
            if token.pos_ in ['ADJ', 'NOUN']:  # Considering adjectives and nouns as descriptors
                descriptors.add(token.text.lower())
    return list(descriptors)

def analyze_response(response):
    doc = nlp(response)
    
    affirmative = any(token.lemma_ in ["yes", "affirmative", "indeed", "absolutely", "certainly", "sure", "definitely", "of course", "yeah", "yep", "yup", "aye", "roger", "uh-huh", "right", "okay", "agreed", "true", "yea", "correct", "alright", "amen", "positively", "undoubtedly", "yah", "yass", "exactly", "naturally", "precisely", "assuredly", "aha", "agreed", "granted", "undoubtedly", "unquestionably", "yesh"] for token in doc)

    negative = any(token.lemma_ in ["no", "negative", "nay", "nope", "nah", "no way", "not", "never", "nix", "uh-uh", "nope", "not at all", "absolutely not", "by no means", "not a chance", "decline", "refuse", "reject", "deny", "veto", "rebuff", "renounce", "repudiate", "retract", "revoke", "withdraw", "non", "none", "nothing", "nowhere", 
    "neither", "null", "void", "zero"] for token in doc)

    return affirmative, negative

def guess_fruit():
    possible_fruits = list(fruit_descriptions.keys())
    descriptors = extract_descriptors(fruit_descriptions)

    # First question to narrow down the possible fruits
    print("Think of a fruit and I'll try to guess it! Describe your fruit: ")
    response = input().strip().lower()
    possible_fruits = [fruit for fruit in possible_fruits if descriptor in fruit_descriptions[fruit]]

    while len(possible_fruits) > 1 and descriptors:
        descriptor = random.choice(descriptors)
        descriptors.remove(descriptor)

        # Determine if the descriptor is a noun or an adjective
        doc = nlp(descriptor)
        pos = doc[0].pos_  # Assuming the descriptor is a single word

        if pos == 'NOUN':
            print(f"The descriptor '{descriptor}' is a noun.")
        elif pos == 'ADJ':
            print(f"The descriptor '{descriptor}' is an adjective.")
        else:
            print(f"The descriptor '{descriptor}' is not a noun or an adjective.")

        question = f"Does the fruit you're thinking of have the characteristic of being {descriptor}?"
        print(question)
        response = input().strip().lower()
        affirmative, negative = analyze_response(response)

        if affirmative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor in fruit_descriptions[fruit]]
        elif negative:
            possible_fruits = [fruit for fruit in possible_fruits if descriptor not in fruit_descriptions[fruit]]
        else:
            print("Sorry, I didn't understand that. Let's try another one.")

    return possible_fruits[0] if possible_fruits else "I couldn't guess the fruit."

# Start the game
fruit_guess = guess_fruit()
print(f"Is it a {fruit_guess}?")
