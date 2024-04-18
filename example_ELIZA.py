from Similarity import Similarity
import os

# Get the list of all .txt files in the Game Modes folder
txt_files = [f for f in os.listdir('Game Modes') if f.endswith('.txt')]

# Define the game modes based on the name of the .txt file(s)
# If there are multiple .txt files, join their names with a comma
game_modes = ', '.join([os.path.splitext(f)[0] for f in txt_files])

print("> Welcome to the guessing game, please select what you want me to guess: " + game_modes)
object_type = input("> ") + ".txt"

# Check if the input is a valid game mode
if object_type not in txt_files:
    print("> Invalid game mode. Please select a valid game mode.")
    exit()

# Read the contents of the file and store each line in the list
object_list = []
file_path = os.path.join('Game Modes', object_type)
with open(file_path, 'r') as file:
    for line in file:
        # Strip any new lines and add to the list
        object_list.append(line.strip())

guesses_made = 0
max_guesses = 3
questions_asked = 0
max_questions = 5
description = ""

similarity = Similarity(object_list, object_type)

# Until the guess is confident (guess_strength => 85), loop 5 times and keep asking for more hints with appended descriptions
# The program gets 3 guesses
while guesses_made < max_guesses and questions_asked < max_guesses:
    
    description += input("> Describe the " + os.path.splitext(object_type)[0] + " you're thinking of: \n> ") + " "
    similarity_scores = similarity.get_guesses(description)
    print(similarity_scores)

    # Check if the guess strength is sufficient
    if similarity_scores[0] == "very strong":
        # Make guess and evaluate user input
        print(f"> Is it '{similarity_scores[1][0]}'?")
        guesses_made += 1
        user_response = input("> ").lower()

        affirmative_responses = ['yes', 'yeah', 'yep', 'correct', 'that\'s right', 'exactly']
        negative_responses = ['no', 'nope', 'nah', 'incorrect', 'wrong', 'not quite']

        if user_response in affirmative_responses:
            print("> Hooray! I guessed it! Thanks for playing.")
            exit()
        elif user_response in negative_responses:
            print("> Oh, sorry to hear that. Let's keep trying.")
        else:
            print("> I'm sorry, I didn't understand your response. Let's keep trying.")
    else:
        print("> Okay, I have some ideas. Give me another hint.")
        questions_asked += 1

# Make final guess
print(f"> Is it '{similarity_scores[1][0]}'?")
user_response = input("> ").lower()

affirmative_responses = ['yes', 'yeah', 'yep', 'correct', 'that\'s right', 'exactly']
negative_responses = ['no', 'nope', 'nah', 'incorrect', 'wrong', 'not quite']

if user_response in affirmative_responses:
    print("> Yay, I guessed it! Thanks for playing.")
    exit()
elif user_response in negative_responses:
    print("> Too bad! Good game.")
else:
    print("> I'm sorry, I didn't understand your response. I'll take it as a win!")
