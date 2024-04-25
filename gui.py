
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread
from PyQt5.QtGui import QColor, QImage, QPalette, QBrush, QTextCursor
from ELIZA_logic import ELIZAGame
from PyQt5 import QtGui

class WorkerThread(QThread):
    # Define a custom signal
    operation_done = pyqtSignal(str)

    def __init__(self, ELIZA_out, game):
        super().__init__()
        self.ELIZA_out = ELIZA_out
        self.game = game
        self.output = None  # Initialize the output attribute

    def run(self):
        # Perform long operations...
        self.output = self.ELIZA_out  # Update the output attribute with the result
        print("WorkerThread: run method completed")  # Debug print statement
        # Emit the custom signal when the run method finishes its execution
        self.operation_done.emit(self.output)

class InteractivePromptGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = ELIZAGame()  # Instance of the game logic class
        self.initUI()
        self.start_game()  # Initialize the game when GUI starts
        self.ELIZA_out = ""

    def initUI(self):
        # Initialize UI components
        self.setWindowTitle('ELIZA Guess Bot')
        self.setGeometry(100, 100, 1400, 800)

        # Set the background image
        palette = QPalette()
        image = QImage("images/background.png")  # Load the image
        image = image.scaled(1400, 800)  # Scale the image to fit the window
        palette.setBrush(QPalette.Background, QBrush(image))
        self.setPalette(palette)

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Text Browser for conversation
        self.text_browser = QTextBrowser(self)
        self.text_browser.setStyleSheet('font-size: 36px; font-weight: bold; color: #FFFFFF; background: transparent')

        # Line Edit for input
        self.line_edit = QLineEdit(self)
        self.line_edit.setStyleSheet('background: transparent; color: #FFFFFF')
        layout.addWidget(self.text_browser)
        layout.addWidget(self.line_edit)

        # Push Button for submitting input
        self.push_button = QPushButton('Submit', self)
        self.push_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.push_button)

        # Connect the Enter key press event to the button click event
        self.line_edit.returnPressed.connect(self.push_button.click)

    def start_game(self):
        # Start the game by displaying a welcome message or similar initial action
        welcome_message = self.game.start_game()
        self.text_browser.append(welcome_message)
        self.game_just_started = True


    def on_button_clicked(self):
        user_input = self.line_edit.text()
        self.text_browser.append(f'> {user_input}')
        self.line_edit.clear()

        if self.game.waiting_for_confirmation:
            if user_input.lower() in ['yes', 'y', 'yeah', 'yep', 'sure', 'right', 'correct']:
                self.text_browser.append("> ELIZA: Woo hoo! Let's play again. Please select a category.")
                self.game = ELIZAGame()  # Restart the game
                self.game_just_started = True
                return
            elif user_input.lower() in ['no', 'n', 'not quite', 'not really', 'incorrect', 'wrong']:
                self.text_browser.append("> ELIZA: Sorry, I couldn't guess it. Let's play again. Please select a category.")
                self.game = ELIZAGame()  # Restart the game
                self.game_just_started = True
                return
            else:
                self.game.waiting_for_confirmation = False
                self.game.last_guess = None

        if self.game_just_started:
            self.ELIZA_out = self.game.select_game_mode(user_input)
            self.game_just_started = False
        else:
            self.ELIZA_out = self.game.play(user_input)

        self.text_browser.append(f'> ELIZA: {self.ELIZA_out}')

    # Update the UI with the output from the game logic or user input
    def update_ui(self, user_input=None):
        if user_input:
            self.text_browser.append(f'> {user_input}')
        else:
            print("Updating UI with:", self.ELIZA_out)
            self.text_browser.append(f'> ELIZA: {self.ELIZA_out}')
            print("done")
        self.text_browser.moveCursor(QTextCursor.End)  # Scroll to the bottom of the text browser

# Example usage
app = QApplication(sys.argv)
ex = InteractivePromptGUI()
ex.show()
sys.exit(app.exec_())
