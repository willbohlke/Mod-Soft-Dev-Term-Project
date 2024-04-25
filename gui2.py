import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread, QUrl
from PyQt5.QtGui import QColor, QImage, QPalette, QBrush, QTextCursor
from ELIZA_logic import ELIZAGame
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
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
        self.setup_audio()
        self.is_muted = False

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
        self.push_button.setStyleSheet("""
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
        self.push_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.push_button)

        # Connect the Enter key press event to the button click event
        self.line_edit.returnPressed.connect(self.push_button.click)

    # Options Button
        self.options_button = QPushButton('Options', self)
        self.options_button.setStyleSheet("""
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
        layout.addWidget(self.options_button)
        self.options_button.clicked.connect(self.toggle_options_frame)

        # options Frame (initially hidden)
        self.options_frame = QFrame(self)
        self.options_frame.setFrameShape(QFrame.StyledPanel)
        self.options_frame.setFixedWidth(400)
        self.options_frame.setFixedHeight(200)
        self.options_frame.move(530, 300)  # Center position
        self.options_frame.setStyleSheet("background-color: #191970;")
        self.options_frame.hide()

        frame_layout = QVBoxLayout(self.options_frame)
        self.mute_button = QPushButton('Mute', self.options_frame)  # Save as an attribute
        self.mute_button.clicked.connect(self.toggle_mute)
        self.mute_button.setStyleSheet("background-color: white;")
        frame_layout.addWidget(self.mute_button)

        restart_button = QPushButton('Restart Game', self.options_frame)
        restart_button.setStyleSheet("background-color: white;")
        restart_button.clicked.connect(self.restart_game)
        frame_layout.addWidget(restart_button)

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

           

    def toggle_options_frame(self):
        self.options_frame.setVisible(not self.options_frame.isVisible())

    def restart_game(self):
        # Clear all game-related text and inputs
        self.text_browser.clear()
        self.line_edit.clear()
        self.line_edit.setEnabled(True)

        self.options_frame.hide()

        # Reinitialize the game logic
        self.game = ELIZAGame()
        self.game_mode_selected = False

        # Start a new game session
        self.start_game()

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.media_player.setMuted(self.is_muted)
        self.mute_button.setText('Unmute' if self.is_muted else 'Mute')


    # sets up audio       
    def setup_audio(self):
        # Create a media player
        self.media_player = QMediaPlayer()
        # Load the audio file
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("sound\Indigo Future Melody.wav")))
        self.media_player.setVolume(20)
        self.media_player.play()
        # Connect the media player's mediaStatusChanged signal to check for end of media playback
        self.media_player.mediaStatusChanged.connect(self.check_media_status)

    def setup_connections(self):
        # Connect the custom signal to restart media playback
        self.media_finished.connect(self.restart_media)

    def check_media_status(self, status):
        # Check if the media playback has reached the end
     if status == QMediaPlayer.EndOfMedia:
        # Restart media playback from the beginning
        self.media_player.setPosition(0)
        self.media_player.play()


    def restart_media(self):
        # Restart media playback from the beginning
        self.media_player.setPosition(0)
        self.media_player.play()    


# To run the application:
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = InteractivePromptGUI()
    mainWin.show()
    sys.exit(app.exec_())