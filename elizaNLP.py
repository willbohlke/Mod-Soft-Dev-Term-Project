import spacy
import random

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

fruit_descriptions = {
    "apple": "A crunchy and sweet fruit that comes in colors ranging from green to red.",
    "mango": "A tropical fruit with a sweet, juicy flesh and smooth, green to yellow skin.",
    "banana": "A long, curved fruit with a yellow skin and soft, sweet flesh.",
    "orange": "A round citrus fruit with a thick, orange skin and a sweet, juicy pulp.",
    "kiwi": "A small, oval fruit with a brown, fuzzy skin and bright green flesh.",
    "strawberry": "A small, red fruit with a sweet flavor and tiny seeds on its surface.",
    "blueberry": "A small, round fruit with a dark blue skin and a sweet, juicy flesh.",
    "grape": "A small, round fruit that grows in clusters and comes in green, red, or purple colors.",
    "watermelon": "A large, round fruit with a green rind and sweet, pink flesh.",
    "pineapple": "A tropical fruit with a spiky, golden skin and sweet, juicy flesh."
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

    while len(possible_fruits) > 1 and descriptors:
        descriptor = random.choice(descriptors)
        descriptors.remove(descriptor)

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
