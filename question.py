import random


# Function to read questions from fruit.txt
def read_fruit_questions():
    with open("Game Modes/fruit.txt", "r") as file:
        questions = file.readlines()
    return [question.strip() for question in questions if question.strip()]  # Remove whitespace and empty lines

fruit_questions = read_fruit_questions()



def fruit_questions(user_description, asked_questions): 
    # Print the user_description
    print("User description:", user_description)

    

    questions = [
        "How does the fruit taste?",
        "Can you estimate the fruit's size? Would you describe it as small, medium, or large?",
        "Does the fruit possess any distinctive traits, such as seeds or a pit?",
        "In terms of its appearance, does the fruit have any unique shapes, such as round or long?",
        "Are there any notable characteristics, such as thorns or a prominent stem, associated with the fruit?",
        "To which botanical family does the fruit belong? For example, is it classified as a melon or citrus?",
        "What color is the inside of the fruit?",
        "How would you describe the texture of the fruit upon biting into it?",
        "What level of firmness does the fruit possess?",
        "Does the fruit require peeling before consumption, or can it be bitten into directly?",
        "Does the fruit have any distinct aroma or fragrance?",
        "What kind of climate is it typically grown in?",
        "What color is the outside of it?",
        "What holiday is it typically associated with your fruit (if any)",
        "What significant vitamins does this fruit contain?", 
        "What season is associated with it?",
        "Is the fruit commonly used in any specific cuisines or dishes?",
        "Is the fruit typically consumed raw, cooked, or used in both ways?"

        ]
    
     # Filter out questions that have already been asked
    new_questions = [question for question in questions if question not in asked_questions]
    random.shuffle(new_questions)

    return new_questions
    

