
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QImage, QPalette, QBrush, QTextCursor
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from example_ELIZA import ELIZAGame

class InteractivePromptGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thinking_dots = 0
        self.game = ELIZAGame()  # Make sure ELIZAGame is properly initialized
        self.initUI()
        self.start_game()  # Start the game when the GUI is initialized
        self.game_mode_selected = False  # Track if a game mode has been selected

    def initUI(self):
        try:
            # Set up the main window
            self.setWindowTitle('ELIZA Guess Bot')
            self.setGeometry(100, 100, 1400, 800)
            
            # Set the background image
            palette = QPalette()
            image = QImage("images/background.png")  # Load the image file
            scaled_image = image.scaled(1400, 800)  # Scale the image to fit the window
            palette.setBrush(QPalette.Background, QBrush(scaled_image))
            self.setPalette(palette)

            # Create central widget and layout
            central_widget = QWidget(self)
            self.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # Text Browser to display conversation
            self.text_browser = QTextBrowser(self)
            text_browser_palette = self.text_browser.palette()
            text_browser_palette.setColor(QPalette.Base, QColor(255, 255, 255, 0))  # Set base color to transparent
            self.text_browser.setPalette(text_browser_palette)
            self.text_browser.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFFFFF")
            layout.addWidget(self.text_browser)
            
            # Line Edit for user input and Button to submit input
            input_layout = QHBoxLayout()
            self.line_edit = QLineEdit(self)
            line_edit_palette = self.line_edit.palette()
            line_edit_palette.setColor(QPalette.Base, QColor(255, 255, 255, 0))  # Set base color to transparent
            self.line_edit.setPalette(line_edit_palette)
            self.line_edit.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFFFFF")
            input_layout.addWidget(self.line_edit)
            self.submit_button = QPushButton('Submit', self)
            self.submit_button.setStyleSheet("""
                QPushButton {
                    background-color: #000080;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px 30px;
                    font-size: 18px;
                    min-width: 250px;
                }
                QPushButton:hover {
                    background-color: #191970; /* Darken color on hover */
                }
            """)
            input_layout.addWidget(self.submit_button)
            layout.addLayout(input_layout)
            
            # Connect button to the function to process input
            self.submit_button.clicked.connect(self.process_input)
            # Connect return key press in line edit to button click
            self.line_edit.returnPressed.connect(self.submit_button.click)

        except Exception as e:
            self.text_browser.append(f"Error in initUI: {e}")

    def start_game(self):
        try:
            start_message = self.game.start_game()  # Get the start message from the game
            self.text_browser.append(f"> ELIZA: {start_message}")
        except Exception as e:
            print(f"Error in start_game: {e}")

    def process_input(self):
        try:
            user_input = self.line_edit.text()
            self.text_browser.append(f"> {user_input}")

            if not self.game_mode_selected:
                # If a game mode hasn't been selected, try to select it
                response = self.game.select_game_mode(user_input)
                if response.startswith("Category selected"):
                    self.game_mode_selected = True
            else:
                # Once a game mode is selected, process input as game play
                response = self.game.play(user_input)

            yes = ["yes", "yep", "yeah", "yup", "certainly", "absolutely", "sure"]
            no = ["no", "nope", "nah", "not", "negative"]
            # Check if the user's input is a synonym for "yes" or "no"
            if "Is it" in response and user_input.lower() in yes:
                self.text_browser.append(f"> ELIZA: Glad I could help!")
                self.line_edit.setDisabled(True)  # Disable user input
                return  # End the game
            elif "Is it" in response and user_input.lower() in no:
                self.text_browser.append(f"> ELIZA: I'm sorry I couldn't guess it. Let's try again!")
                self.line_edit.setDisabled(True)  # Disable user input
                return  # End the game
            else:
                self.text_browser.append(f"> ELIZA: {response}")
            self.line_edit.clear()
        except Exception as e:
            self.text_browser.append(f"Error in process_input: {e}")

# To run the application:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = InteractivePromptGUI()
    mainWin.show()
    sys.exit(app.exec_())