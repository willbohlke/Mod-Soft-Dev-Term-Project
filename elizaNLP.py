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
    "apple": "A crunchy and sweet fruit that comes in colors ranging from green to red. Often eaten raw or used in desserts.",
    "banana": "A long, curved fruit with a yellow skin and soft, sweet flesh. Often eaten raw or used in baking.",
    "orange": "A round citrus fruit with a bright orange skin and sweet, juicy flesh. Commonly eaten fresh or juiced.",
    "mango": "A tropical fruit with a sweet, juicy flesh and smooth, green to yellow skin. Commonly eaten fresh or used in smoothies.",
    "cherry": "A small, round fruit with a bright red or black skin and a sweet or tart taste. Often used in desserts or as a garnish.",
    "grape": "A small, juicy fruit that comes in various colors and is often used to make wine or eaten as a snack.",
    "lemon": "A sour citrus fruit with a yellow skin and acidic juice. Commonly used in cooking and for its refreshing flavor.",
    "pineapple": "A tropical fruit with a spiky, rough skin and sweet, juicy flesh. Often used in desserts or as a topping.",
    "strawberry": "A small, red fruit with a sweet and tangy flavor. Commonly used in desserts, jams, and as a topping.",
    "blueberry": "A small, round fruit with a dark blue or purple skin and a sweet taste. Often used in baking or eaten as a snack.",
    "raspberry": "A small, red fruit with a sweet and slightly tart taste. Commonly used in desserts, jams, and as a topping.",
    "kiwi": "A small, oval fruit with a brown, fuzzy skin and green flesh. Known for its tangy and sweet flavor.",
    "watermelon": "A large, juicy fruit with a green rind and sweet, red flesh. Often eaten fresh or used in fruit salads.",
    "melon": "A large, round fruit with a smooth skin and sweet, juicy flesh. Commonly eaten fresh or used in fruit salads.",
    "blackberry": "A small, dark purple fruit with a sweet and tart taste. Often used in desserts, jams, and as a topping.",
    "pear": "A sweet and juicy fruit with a thin skin and a shape that varies from round to pear-shaped. Often eaten fresh or used in desserts.",
    "peach": "A soft, juicy fruit with a fuzzy skin and a sweet, fragrant flavor. Commonly eaten fresh or used in desserts.",
    "plum": "A small, round fruit with a smooth skin and a sweet or tart taste. Often eaten fresh or used in desserts.",
    "fig": "A small, pear-shaped fruit with a thin skin and sweet, chewy flesh. Commonly eaten fresh or dried.",
    "pomegranate": "A round fruit with a thick, leathery skin and juicy, ruby-red seeds. Known for its sweet and tart flavor.",
    "coconut": "A large, brown fruit with a hard, hairy shell and sweet, creamy flesh. Commonly used in cooking and for its milk and oil.",
    "lime": "A small, green citrus fruit with a sour and acidic taste. Commonly used in cooking and for its refreshing flavor.",
    "apricot": "A small, orange fruit with a smooth skin and a sweet, slightly tart taste. Often eaten fresh or used in desserts.",
    "dragon fruit": "A tropical fruit with a vibrant pink or yellow skin and white or red flesh speckled with black seeds. Known for its mild, sweet flavor.",
    "nectarine": "A smooth-skinned fruit similar to a peach but with a firmer texture and a slightly tart taste. Often eaten fresh or used in desserts.",
    "guava": "A tropical fruit with a green or yellow skin and sweet, juicy flesh. Commonly eaten fresh or used in jams and jellies.",
    "lychee": "A small, round fruit with a rough, pinkish-red skin and sweet, translucent flesh. Often eaten fresh or used in desserts.",
    "tangerine": "A small, citrus fruit with a bright orange skin and sweet, juicy flesh. Commonly eaten fresh or used in salads and desserts.",
    "passion fruit": "A round or oval fruit with a thick, purple or yellow skin and a tart, tropical flavor. Often used in desserts and beverages."
}

def guess_fruit():
    possible_fruits = list(fruit_descriptions.keys())
    while len(possible_fruits) > 1:
        clue = input("Describe the fruit or answer the question: ")
        doc = nlp(clue)
        keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

        # Filter possible fruits based on the clue/description
        possible_fruits = [fruit for fruit in possible_fruits if any(keyword in fruit_descriptions[fruit] for keyword in keywords)]

        if len(possible_fruits) > 1:
            print(f"Possible fruits: {possible_fruits}")
            # Here you can implement logic to ask questions based on the remaining fruits
            # For example, if most remaining fruits are red, ask if the fruit is red

    return possible_fruits[0] if possible_fruits else "I couldn't guess the fruit."

# Start the game
fruit_guess = guess_fruit()
print(f"My guess is: {fruit_guess}")