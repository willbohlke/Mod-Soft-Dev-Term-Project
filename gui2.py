
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget
from example_ELIZA import ELIZAGame

class InteractivePromptGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game = ELIZAGame()  # Make sure ELIZAGame is properly initialized
        self.initUI()
        self.start_game()  # Start the game when the GUI is initialized
        self.game_mode_selected = False  # Track if a game mode has been selected

    def initUI(self):
        try:
            # Set up the main window
            self.setWindowTitle('Interactive Terminal Prompt')
            self.setGeometry(100, 100, 480, 320)
            
            # Create central widget and layout
            central_widget = QWidget(self)
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # Text Browser to display conversation
            self.text_browser = QTextBrowser(self)
            layout.addWidget(self.text_browser)
            
            # Line Edit for user input
            self.line_edit = QLineEdit(self)
            layout.addWidget(self.line_edit)
            
            # Button to submit input
            self.submit_button = QPushButton('Submit', self)
            layout.addWidget(self.submit_button)
            
            # Connect button to the function to process input
            self.submit_button.clicked.connect(self.process_input)

            self.show()  # Ensure the window is shown
        except Exception as e:
            print(f"Error in initUI: {e}")

    def start_game(self):
        try:
            start_message = self.game.start_game()  # Get the start message from the game
            self.text_browser.append(f"ELIZA: {start_message}")
        except Exception as e:
            print(f"Error in start_game: {e}")

    def process_input(self):
        try:
            user_input = self.line_edit.text()
            self.text_browser.append(f"User: {user_input}")
            if not self.game_mode_selected:
                # If a game mode hasn't been selected, try to select it
                response = self.game.select_game_mode(user_input)
                if response.startswith("> Category selected"):
                    self.game_mode_selected = True
            else:
                # Once a game mode is selected, process input as game play
                response = self.game.play(user_input)
            
            if response:
                self.text_browser.append(f"ELIZA: {response}")
            self.line_edit.clear()
        except Exception as e:
            self.text_browser.append(f"Error in process_input: {e}")

# To run the application:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = InteractivePromptGUI()
    mainWin.show()
    sys.exit(app.exec_())
