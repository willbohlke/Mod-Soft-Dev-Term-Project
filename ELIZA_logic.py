
from Similarity import Similarity
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
import threading
import os

class ELIZAGame(QObject):
    stop_timer_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
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
        self.thinking_dots = 0
        self.stop_timer_signal.connect(self.stop_timer)

    def start_game(self):
        return "Welcome to the ELIZA Guess Bot, please enter what you want me to guess: " + self.game_modes

    def select_game_mode(self, game_mode):
        self.object_type = game_mode + ".txt"
        if self.object_type not in self.txt_files:
            return "Invalid selection. Please select a valid category."
        file_path = os.path.join('Game Modes', self.object_type)
        with open(file_path, 'r') as file:
            for line in file:
                self.object_list.append(line.strip())
        self.similarity = Similarity(self.object_list, self.object_type)
        return "Category selected. Describe the " + self.object_type[:-4] + " you're thinking of."

    def play(self, description):
        if not self.similarity:
            return "> Error: Game mode not properly initialized or similarity object not created."
        self.description += description + " "

        # Start the thinking animation
        self.thinking_timer = QTimer()
        self.thinking_timer.timeout.connect(self.update_thinking_animation)
        self.thinking_timer.start(500)  # Update the animation every 500 ms

        # Define the function to run in a separate thread
        def get_guesses_thread():
            self.guess_strength, self.top_guesses = self.similarity.get_guesses(self.description)
            self.stop_timer_signal.emit()  # Emit the signal to stop the timer
            self.guesses_ready.set()  # Set the event to signal that the guesses are ready

        # Create and start the thread
        self.guesses_ready = threading.Event()
        thread = threading.Thread(target=get_guesses_thread)
        thread.start()

        # Wait for the guesses to be ready
        self.guesses_ready.wait()

        top_guess = self.top_guesses[0][0]

        while self.questions_asked < self.max_questions:
            # guess_strength, top_guesses = self.similarity.get_guesses(self.description)
            self.questions_asked += 1
            remaining = str(self.max_questions - self.questions_asked)

            if self.guess_strength == 'strong':
                return f"Is it {top_guess}?"
            elif self.guess_strength == 'moderate':
                output = "I almost got it! Describe it more: (" + remaining + " remaining)"
            elif self.guess_strength == 'weak':
                output = "I have a vague idea, give me another hint: (" + remaining + " remaining)"
            return output
        
        return f"Is it {top_guess}?"
    
    def stop_timer(self):
        self.thinking_timer.stop()
    
    def update_thinking_animation(self):
        # Update the thinking animation
        self.thinking_dots += 1
        if self.thinking_dots > 3:
            self.thinking_dots = 0
        self.thinking_text = "Thinking" + "." * self.thinking_dots
        return self.thinking_text
    
    
    

# Removed the direct execution part to ensure it doesn't conflict with the GUI
