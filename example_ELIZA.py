
from Similarity import Similarity
from Similarity import get_guesses
import os

# Get the list of all .txt files in the Game Modes folder
def get_game_modes():
    txt_files = [f for f in os.listdir('Game Modes') if f.endswith('.txt')]
    game_modes = [os.path.splitext(f)[0] for f in txt_files]
    return game_modes

def main(gm=None, gui=False, output_func=print, input_func=input):
    game_modes = get_game_modes()

    if gm is not None:
        object_type = gm + ".txt"
    else:
        output_func("> Welcome to the guessing game, please select what you want me to guess: " + ', '.join(game_modes))
        object_type = input_func("> ") + ".txt"

    if object_type not in [gm + '.txt' for gm in game_modes]:
        output_func("> Invalid game mode. Please select a valid game mode.")
        return

    object_list = []
    file_path = os.path.join('Game Modes', object_type)
    with open(file_path, 'r') as file:
        for line in file:
            object_list.append(line.strip())

    guesses_made = 0
    max_guesses = 3
    questions_asked = 0
    max_questions = 5
    description = ""

    similarity = Similarity(object_list, object_type)

    while guesses_made < max_guesses and questions_asked < max_questions:
        if not gui:
            description += input_func("> Describe the " + os.path.splitext(object_type)[0] + " you're thinking of: \n> ") + " "
        similarity_scores = similarity.get_guesses(description)
        output_func(str(similarity_scores))
        guesses_made += 1
        questions_asked += 1

        if similarity_scores[0] == "very strong":
            output_func(f"> Is it '{similarity_scores[1][0]}'?")
            guesses_made += 1
            user_response = input_func("> ").lower()

            affirmative_responses = ['yes', 'yeah', 'yep', 'correct', "that's right", 'exactly']
            negative_responses = ['no', 'nope', 'nah', 'incorrect', 'wrong', 'not quite']

            if user_response in affirmative_responses:
                output_func("> Hooray! I guessed it! Thanks for playing.")
                return
            elif user_response in negative_responses:
                output_func("> Oh, sorry to hear that. Let's keep trying.")
            else:
                output_func("> I'm sorry, I didn't understand your response. Let's keep trying.")
        else:
            output_func("> Okay, I have some ideas. Give me another hint.")
            questions_asked += 1

    output_func(f"> Is it '{similarity_scores[1][0]}'?")
    user_response = input_func("> ").lower()

    affirmative_responses = ['yes', 'yeah', 'yep', 'correct', "that's right", 'exactly']
    negative_responses = ['no', 'nope', 'nah', 'incorrect', 'wrong', 'not quite']

    if user_response in affirmative_responses:
        output_func("> Yay, I guessed it! Thanks for playing.")
    elif user_response in negative_responses:
        output_func("> Too bad! Good game.")
    else:
        output_func("> I'm sorry, I didn't understand your response. I'll take it as a win!")

if __name__ == "__main__":
    main()
