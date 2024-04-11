import pytest
import spacy
import random

from elizaNLP import analyze_response, extract_descriptors

# Load the small spacy model for testing
nlp = spacy.load("en_core_web_sm")

@pytest.fixture
def sameple_fruit():
    return"apple"

@pytest.fixture
def sample_description():
    return "red sweet"

def test_guess_fruit_success(sample_fruit, sample_description):
    #Simulate user input
    def mock_input(prompt):
        return sample_description
    #Patch the input function to return our sample description
    with pytest.monkeypatch.context() as m:
        m.setattr("builtins.input", mock_input)
        result = guess_fruit()
        assert result == sample_fruit

def test_guess_fruit_no_matches():
    def mock_input(prompt):
        return "purple spiky"
    with pytest.monkeypatch.context() as m:
        m.setattr("builtins.input", mock_input)
        result = guess_fruit()
        assert result == "I couldn't guess the fruit."

#  *** MAIN FRUIT GUESSING SCRIPT ***
# ... Include your fruit_descriptions dictionary and guess_fruit function here ....
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


# Start the game (only runs if this script is directly executed, not during testing)
if __name__ == "__main__":
    fruit_guess = guess_fruit()
    print(f"My guess is: {fruit_guess}")
