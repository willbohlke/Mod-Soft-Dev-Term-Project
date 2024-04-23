
from Similarity import Similarity
import os

class ELIZAGame:
    def __init__(self):
        self.txt_files = [f for f in os.listdir('Game Modes') if f.endswith('.txt')]
        self.game_modes = ', '.join([os.path.splitext(f)[0] for f in self.txt_files])
        self.object_type = None
        self.object_list = []
        self.guesses_made = 0
        self.max_guesses = 3
        self.questions_asked = 1
        self.max_questions = 5
        self.description = ""
        self.similarity = None
        self.similarity_scores = []

    def start_game(self):
        return "> Welcome to the guessing game, please select what you want me to guess: " + self.game_modes

    def select_game_mode(self, game_mode):
        self.object_type = game_mode + ".txt"
        if self.object_type not in self.txt_files:
            return "> Invalid selection. Please select a valid category."
        file_path = os.path.join('Game Modes', self.object_type)
        with open(file_path, 'r') as file:
            for line in file:
                self.object_list.append(line.strip())
        self.similarity = Similarity(self.object_list, self.object_type)
        return "> Category selected. Describe the " + self.object_type + " you're thinking of."

    def play(self, description):
        if not self.similarity:
            return "> Error: Game mode not properly initialized or similarity object not created."
        self.description += description + " "
        guess_strength, top_guesses = self.similarity.get_guesses(self.description)
        top_guess = top_guesses[0][0]

        while self.questions_asked < self.max_questions:
            # guess_strength, top_guesses = self.similarity.get_guesses(self.description)
            self.questions_asked += 1
            remaining = str(self.max_questions - self.questions_asked)

            if guess_strength == 'strong':
                return f"> Is it {top_guess}?"
            elif guess_strength == 'moderate':
                output = "I almost got it! Describe it more: (" + remaining + " remaining)"
            elif guess_strength == 'weak':
                output = "I have a vague idea, give me another hint: (" + remaining + " remaining)"
            return output
        
        return f"> is it {top_guess}?"

# Removed the direct execution part to ensure it doesn't conflict with the GUI
