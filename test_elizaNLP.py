import pytest
import nltk

from nltk.corpus import wordnet as wn
from elizaNLP import extract_descriptors, analyze_response, guess_fruit
from similar import FruitSimilarity


# Patch spacy.load with the mock fixture
def test_extract_descriptors():
    # Sample fruit descriptions
    fruit_descriptions = {
        "apple": ["sweet", "tart", "sour", "crisp", "green", "red"],
    }

    # Expected descriptors
    expected_descriptors = ["sweet", "tart", "sour", "crisp", "green"]

    # Test the function
    descriptors = extract_descriptors(fruit_descriptions)

    # Assert that the extracted descriptors match the expected ones
    assert set(descriptors) == set(expected_descriptors)


def test_analyze_response():
    # Test affirmative response
    affirmative_response = "yes for sure"
    affirmative, negative, unsure = analyze_response(affirmative_response)
    assert affirmative and not negative and not unsure

    # Test negative response
    negative_response = "no way"
    affirmative, negative, unsure = analyze_response(negative_response)
    assert not affirmative and negative and not unsure

    # # Test unsure response
    unsure_response = "maybe"
    affirmative, negative, unsure = analyze_response(unsure_response)
    assert not affirmative and not negative and unsure  # Updated assertion for unsure response


def test_guess_fruit(monkeypatch):
    # Define mock user input
    user_input = iter(["yes", "no", "yes", "yes", "yes"])  # Add more input values as needed

    # Mock input() function to return user_input values
    def mock_input():
        return next(user_input)

    # Apply the patch
    monkeypatch.setattr('builtins.input', mock_input)

    # Call the function and check the result
    fruit_guess = guess_fruit()
    assert fruit_guess == "> I couldn't guess the fruit."


def mock_wn_synsets(fruit):
    # Simulate some basic synset results
    synsets = []
    if fruit == "apple":
        synsets.append(wn.Synset("fruit.n.01"))  # Mock a synset with fruit definition
    return synsets


wn.synsets = mock_wn_synsets  # Replace actual wn.synsets with mock


class TestFruitSimilarity:

    def test_get_fruit_definitions_with_definition(self):  # Test with actual wn.synsets
        fruits = ["apple", "banana"]
        fruit_similarity = FruitSimilarity(fruits)
        fruit_definitions = fruit_similarity.get_fruit_definitions()

        assert len(fruit_definitions) == 1  # Only apple should have definition
        assert "apple" in fruit_definitions
        assert isinstance(fruit_definitions["apple"], str)  # Definition should be a string

    def test_get_fruit_definitions_without_definition(self):  # Test with actual wn.synsets
        fruits = ["banana"]
        fruit_similarity = FruitSimilarity(fruits)
        fruit_definitions = fruit_similarity.get_fruit_definitions()

        assert len(fruit_definitions) == 0  # No definition found for banana

    def test_calculate_similarity(self):  # Test (unchanged)
        fruits = ["apple", "orange"]
        fruit_similarity = FruitSimilarity(fruits)
        user_description = "A sweet, red fruit"
        similarity_scores = fruit_similarity.calculate_similarity(user_description)

        assert len(similarity_scores) == 2  # Scores for both fruits
        assert similarity_scores[0][0] == "apple"  # Apple should be more similar due to "red"
        assert similarity_scores[1][0] == "orange"
