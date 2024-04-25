
import os
from Similarity import Similarity

class ELIZAGame():
    def __init__(self):
        self.txt_files = [f for f in os.listdir('Game Modes') if f.endswith('.txt')]
        self.game_modes = {os.path.splitext(f)[0]: None for f in self.txt_files}  # Store game modes and their data
        self.object_type = None
        self.guesses_made = 0
        self.max_guesses = 3
        self.questions_asked = 0
        self.max_questions = 5
        self.user_in = ""
        self.similarity = None
        self.thinking_dots = 0
        self.waiting_for_confirmation = False
        self.last_guess = None

        # question bank
        self.question_bank = {
            'film': [
                "Tell me about the genre of the film.",
                "Who are some people who worked on the film?",
                "Who are the main actors or character in the film?",
                "When was the film released?",
                "What series or franchise is the film part of?"
            ],
            'book': [
                "Tell me about the genre of the book.",
                "Who is the author of the book? Have they written anything else?",
                "When was the book published?",
                "What series is the book part of? Or is it a stand-alone?",
                "What is the main theme of the book?"
            ],
            'celebrity': [
                "What is the profession of the celebrity?",
                "What gender is this celebrity?",
                "What kind of roles has this celebrity had?",
                "What events are this celebrity known for?",
                "What achievements does this celebrity have?"
            ]
        }

    def start_game(self):
        available_modes = ', '.join(self.game_modes.keys())
        return f"> Welcome to the ELIZA Guess Bot, I will guess a {available_modes} that you're thinking of in 5 responses or less! \n> Please enter what you want me to guess: " + available_modes

    def select_game_mode(self, game_mode):
        if game_mode not in self.game_modes:
            return f"Invalid selection. Please select a valid category from {list(self.game_modes.keys())}."

        if self.game_modes[game_mode] is None:  # Load game mode data if not already loaded
            file_path = os.path.join('Game Modes', game_mode + '.txt')
            if not os.path.exists(file_path):
                return f"Error: The file for {game_mode} does not exist at {file_path}."
            with open(file_path, 'r') as file:
                self.game_modes[game_mode] = [line.strip() for line in file]

        self.object_list = self.game_modes[game_mode]
        self.object_type = game_mode
        try:
            self.similarity = Similarity(self.object_list, self.object_type)
        except Exception as e:
            return f"Failed to create a similarity object: {str(e)}"
        
        return f"Category '{game_mode}' selected. To start, give me a brief summary of the {game_mode} you're thinking of:"

    def play(self, user_in):
        if not self.similarity:
            return "Error: Game mode not properly initialized or similarity object not created."
        self.user_in += user_in + " "
        return self.process_input(user_in)     
    
    def process_input(self, user_input):
        if self.waiting_for_confirmation:
            if user_input.lower() in ['yes', 'y', 'yeah', 'yep', 'sure', 'right', 'correct']:
                self.waiting_for_confirmation = False
                self.last_guess = None
                return "Woo hoo! Let's play again. Please select a category."
            else:
                self.waiting_for_confirmation = False
                self.last_guess = None
                remaining_questions = self.max_questions - self.questions_asked
                return f"Darn! I'll get it next time!"

        guess, score = self.similarity.get_guesses(user_input)
        self.questions_asked += 1

        print(self.user_in)
        print(f"{guess} {score}")


        if self.questions_asked >= self.max_questions:
            self.last_guess = guess
            self.waiting_for_confirmation = True
            return f"Maximum number of questions reached. Is it {guess}?"

        if score > 0.25:
            self.waiting_for_confirmation = True
            self.last_guess = guess
            return f"Is it {guess}?"
        else:
            remaining_questions = self.max_questions - self.questions_asked
            # choose a random question from the question bank that mathces the object type
            question = self.question_bank[self.object_type][self.questions_asked]
            return f"{question} ({remaining_questions} remaining):"


# Example usage to debug
# game = ELIZAGame()
# print(game.start_game())
# response = game.select_game_mode('film')
# print(response)
# if 'Failed' not in response:
#     print(game.play('A description of something'))
