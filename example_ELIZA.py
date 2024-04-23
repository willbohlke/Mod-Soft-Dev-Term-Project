
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
        self.questions_asked = 0
        self.max_questions = 5
        self.description = ""
        self.similarity = None
        self.similarity_scores = []

    def start_game(self):
        return "> Welcome to the guessing game, please select what you want me to guess: " + self.game_modes

    def select_game_mode(self, game_mode):
        self.object_type = game_mode + ".txt"
        if self.object_type not in self.txt_files:
            return "> Invalid game mode. Please select a valid game mode."
        file_path = os.path.join('Game Modes', self.object_type)
        with open(file_path, 'r') as file:
            for line in file:
                self.object_list.append(line.strip())
        self.similarity = Similarity(self.object_list, self.object_type)
        return "> Game mode selected. Describe the object you're thinking of."

    def play(self, description):
        if not self.similarity:
            return "> Error: Game mode not properly initialized or similarity object not created."
        
        self.description += description + " "
        if self.guesses_made < self.max_guesses and self.questions_asked < self.max_questions:
            self.similarity_scores = self.similarity.get_guesses(self.description)
            self.questions_asked += 1
            return self.similarity_scores
        elif self.guesses_made >= self.max_guesses or self.questions_asked >= self.max_questions:
            return "> No more guesses or questions allowed."

# Removing the direct execution part to ensure it doesn't conflict with the GUI
