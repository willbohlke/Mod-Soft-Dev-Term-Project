import pytest
from elizaNLP import extract_descriptors, analyze_response, guess_fruit


# Define test cases for extract_descriptors function
def test_extract_descriptors():
    fruit_descriptions = {
        "apple": ["sweet", "sour", "crisp", "green", "red"],
        "mango": ["sweet", "soft", "tropical", "yellow", "orange", "red"],
        "banana": ["sweet", "creamy", "yellow"],
        "blueberry": ["sweet", "small", "purple", "blue"],
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
        "orange": ["sour", "citrusy", "orange"],
        "lemon": ["sour", "citrusy", "refreshing", "yellow"],
        "lime": ["sour", "citrusy", "refreshing", "green"]
    }
    descriptors = extract_descriptors(fruit_descriptions)
    expected_descriptors = ["sweet", "sour", "crisp", "green", "red"]
    assert set(descriptors) == set(expected_descriptors)


# Define test cases for analyze_response function
@pytest.mark.parametrize("response, expected", [
    ("Yes, it is.", (True, False)),
    ("No, it isn't.", (False, True)),
    ("Maybe.", (False, False)),
])
def test_analyze_response(response, expected):
    assert analyze_response(response) == expected


# Define test cases for guess_fruit function
def test_guess_fruit(monkeypatch):
    # Define mock user input
    user_input = iter(["yes", "no", "yes", "yes", "no"])  # Add more input values as needed

    # Mock input() function to return user_input values
    def mock_input():
        return next(user_input)

    # Apply the patch
    monkeypatch.setattr('builtins.input', mock_input)

    # Call the function and check the result
    fruit_guess = guess_fruit()
    assert fruit_guess == "I couldn't guess the fruit."


# Run tests
if __name__ == "__main__":
    pytest.main()
