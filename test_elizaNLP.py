import pytest
import spacy

#Replace with the correct path to your fruit guessing script
from your_script import fruit_descriptions, guess_fruit

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

# Start the game (only runs if this script is directly executed, not during testing)
if __name__ = "__main__":
    fruit_guess = guess_fruit()
    print(f"My guess is: {fruit_guess}")