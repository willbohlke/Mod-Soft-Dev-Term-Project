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
        # Strip any newlines and add to the list
        object_list.append(line.strip())

while True:
    similarity = Similarity(object_list, object_type)
    user_desc = input("> Enter a description of the " + os.path.splitext(object_type)[0] + " you're thinking of: \n> ")
    similarity_scores = similarity.get_guesses(user_desc)
    print(similarity_scores)

    # Receive user input here and check for various responses
    print(f"> Is it a {similarity_scores[1][0]}?")
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