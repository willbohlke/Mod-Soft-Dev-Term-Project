from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from question import fruit_questions 
import sys

class BackgroundWidget(QWidget):
    def __init__(self, background_image):
        super().__init__()
        self.background_label = QLabel(self)
        pixmap = QPixmap(background_image)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

class MainWindow(QWidget):

    media_finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guess What?")
        self.setFixedSize(1400, 800)
        self.setup_ui()
        self.setup_audio()

    def setup_ui(self):
        # Set up the background image
        self.background_label = QLabel(self)
        pixmap = QPixmap("images/background.png")  
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 1400, 800) 


        # Mute icon
        self.mute_icon_label = QLabel(self)
        self.mute_icon_label.setPixmap(QPixmap("images/mute_icon.png").scaled(80, 80, Qt.KeepAspectRatio))  # Set icon
        self.mute_icon_label.setFixedSize(100, 100)
        self.mute_icon_label.setStyleSheet("""
            QLabel {
                background-color: transparent; /* Background color */
                border: none;
                border-radius: 20px; /* Rounded border */
                padding: 10px; /* Padding */
            }
        """)
        self.mute_icon_label.move(20, 20)
        self.mute_icon_label.raise_()


        # Set up the main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
    

        # Start frame
        self.start_frame = QWidget(self)
        self.start_frame_layout = QVBoxLayout(self.start_frame)
        self.start_frame_layout.setAlignment(Qt.AlignCenter)

        # Welcome text
        self.start_text1 = QLabel("Welcome!", self.start_frame)
        self.start_text1.setAlignment(Qt.AlignCenter)
        self.start_text1.setStyleSheet("font-size: 36px; font-weight: bold; color: #FFFFFF; margin-bottom: 20px")
        self.start_frame_layout.addWidget(self.start_text1)

        # Game mode button
        self.game_mode_button = QPushButton("Game Mode", self.start_frame)
        self.game_mode_button.setStyleSheet("""
            QPushButton {
                background-color: #000080;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
                min-width: 400px;
            }
            QPushButton:hover {
                background-color: #191970; /* Darken color on hover */
            }
        """)
        self.game_mode_button.clicked.connect(self.game_mode)
        self.start_frame_layout.addWidget(self.game_mode_button)

        self.main_layout.addWidget(self.start_frame)

        # Game mode frame
        self.game_mode_frame = QWidget(self)
        self.game_mode_frame_layout = QVBoxLayout(self.game_mode_frame)
        self.game_mode_frame_layout.setAlignment(Qt.AlignCenter)

        # Choose game mode text
        self.game_mode_message = QLabel("Please choose a game mode", self.game_mode_frame)
        self.game_mode_message.setAlignment(Qt.AlignCenter) 
        self.game_mode_message.setStyleSheet("font-size: 24px; color: #FFFFFF;")
        self.game_mode_frame_layout.addWidget(self.game_mode_message)

        # Fruit guesser button
        self.fruit_guesser_button = QPushButton("Fruit Guesser", self.game_mode_frame)
        self.fruit_guesser_button.setStyleSheet("""
            QPushButton {
                background-color: #000080;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
                min-width: 400px;
            }
            QPushButton:hover {
                background-color: #191970; /* Darken color on hover */
            }
        """)
        self.fruit_guesser_button.clicked.connect(self.start_game)
        self.game_mode_frame_layout.addWidget(self.fruit_guesser_button)


        # Hide game mode frame initially
        self.game_mode_frame.hide()

        self.main_layout.addWidget(self.game_mode_frame)

        # Game frame
        self.game_frame = QWidget(self)
        self.game_frame_layout = QVBoxLayout(self.game_frame)
        self.game_frame_layout.setAlignment(Qt.AlignCenter)

        # Create a horizontal layout to center the widgets
        self.center_layout = QHBoxLayout()  # Define center layout
        self.center_layout.setAlignment(Qt.AlignCenter)

        # Question label
        self.question_label = QLabel(self.game_frame)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("font-size: 18px; color: #009688;")
        self.game_frame_layout.addWidget(self.question_label)

        # Add a vertical layout for the chat box and answer entry
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignCenter)

        # Chat box
        self.chat_box = QTextEdit(self.game_frame)
        self.chat_box.setReadOnly(True)
        self.chat_box.setFixedHeight(350)  # Set fixed height
        self.chat_box.setFixedWidth(650)  # Set fixed width
       
        # Set font size
        font = self.chat_box.font()
        font.setPointSize(10)  # Adjust the font size as needed
        self.chat_box.setFont(font)

        self.chat_box.setStyleSheet("""
             QTextEdit {
                  border: 2px solid #FF00FF; /* Neon purple border */
                    border-radius: 10px; /* Rounded corners */
                    padding: 5px; /* Add padding */
                    background-color: #4B0082;
                    color: #FFFFFF;
                }
                QTextEdit:focus {
                    border: 2px solid #FF00FF; /* Neon purple border on focus */
                }
                QTextEdit {
                    border-bottom: 5px solid rgba(0,0,0,0.1); /* Add shadow */
                    border-right: 5px solid rgba(0,0,0,0.1); /* Add shadow */
                }
            """)
        self.chat_layout.addWidget(self.chat_box)

        # Answer entry box
        self.answer_entry = QLineEdit(self.game_frame)
        self.answer_entry.setFixedWidth(650)
        self.answer_entry.setFixedHeight(60)

        font = self.answer_entry.font()
        font.setPointSize(12) 
        self.answer_entry.setFont(font)

        self.answer_entry.setStyleSheet("""
            QLineEdit {
              border: 2px solid #FF00FF; /* Neon purple border */
                border-radius: 10px; /* Rounded corners */
                background-color: #4B0082;
                color: #FFFFFF;
            }
            QLineEdit:focus {
                border: 2px solid #FF00FF; /* Neon purple border on focus */
            }
            QLineEdit {
                border-bottom: 5px solid rgba(0,0,0,0.1); /* Add shadow */
                border-right: 5px solid rgba(0,0,0,0.1); /* Add shadow */
            }
        """)
        self.chat_layout.addWidget(self.answer_entry)

        self.center_layout.addLayout(self.chat_layout)  # Add chat layout to center layout
        self.game_frame_layout.addLayout(self.center_layout)  # Add center layout to game frame layout

           # Quit game button
        self.quit_game_button = QPushButton("Quit Game", self.game_frame)
        self.quit_game_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
                max-width: 100px;
            }
            QPushButton:hover {
                background-color: #8B0000; /* Darken color on hover */
            }
        """)
        self.quit_game_button.clicked.connect(self.quit_game)
        self.game_frame_layout.addWidget(self.quit_game_button)
        self.game_frame_layout.addWidget(self.quit_game_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        # Hide game frame initially
        self.game_frame.hide()

        self.main_layout.addWidget(self.game_frame)

         # Create the volume slider
        self.volume_slider = QSlider(Qt.Vertical, self.game_frame)
        self.volume_slider.setParent(self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)  # Initial volume set to maximum
        self.volume_slider.valueChanged.connect(self.adjust_volume)
        self.volume_slider.setGeometry(55, 110, 30, 200)  # Adjust the position of the volume slider
        self.volume_slider.raise_()


    def setup_audio(self):
        # Create a media player
        self.media_player = QMediaPlayer()
        # Load the audio file
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile("sound\Indigo Future Melody.wav")))
        self.media_player.play()
        # Connect the media player's mediaStatusChanged signal to check for end of media playback
        self.media_player.mediaStatusChanged.connect(self.check_media_status)

    def check_media_status(self, status):
        # Check if the media playback has reached the end
     if status == QMediaPlayer.EndOfMedia:
        # Restart media playback from the beginning
        self.media_player.setPosition(0)
        self.media_player.play()


    def start_game(self):
        print("Starting the game...")
        # Hide game mode frame
        self.game_mode_frame.hide()
        # Show game frame
        self.game_frame.show()
        # Start the fruit guessing game
        self.play_game()

    def setup_connections(self):
        # Connect the custom signal to restart media playback
        self.media_finished.connect(self.restart_media)

    def restart_media(self):
        # Restart media playback from the beginning
        self.media_player.setPosition(0)
        self.media_player.play()    

    def game_mode(self):
        print("Entering game mode...")
        # Hide start frame
        self.start_frame.hide()
        # Show game mode frame
        self.game_mode_frame.show()

    def play_game(self):
        print("Starting the game...")
        # Hide game mode frame
        self.game_mode_frame.hide()
        # Show game frame
        self.game_frame.show()
        # Start the fruit guessing game
        self.user_description = ""  # Reset user description
        self.asked_questions = []   # Initialize asked questions list
        self.update_output("System", "Think of a fruit and I'll try to guess it! Describe your fruit: ")
        self.answer_entry.show()
        self.answer_entry.returnPressed.connect(lambda: self.process_response(self.answer_entry.text()))
        # Call fruit_questions with an empty user description and an empty list of asked questions
        self.questions = fruit_questions("", [])


    def process_response(self, response):
        print("User response:", response)

        # Append the user's response to the user_description string
        self.user_description += " " + response

        # Append the user's response to the chat box
        self.update_output("User", response)

        # Pass the user_description string to fruit_questions, along with asked questions
        self.questions = fruit_questions(self.user_description.strip(), self.asked_questions)

        # Display the next question from the list of questions
        if self.questions:
            next_question = self.questions.pop(0)
            self.asked_questions.append(next_question)  # Add the new question to the list of asked questions
            self.update_output("System", next_question)
        else:
            # If there are no more questions, hide the answer entry
            self.answer_entry.hide()

        # Clear the answer entry for the next question
        self.answer_entry.clear()
        
    def update_output(self, sender, message):
        self.chat_box.append(f"{sender}: {message}")


    def quit_game(self):
        print("Quitting the game...")
        # Hide the game frame
        self.game_frame.hide()
        # Show the start frame
        self.start_frame.show()
        # Clear the chat box
        self.chat_box.clear()

    def adjust_volume(self, volume_level):
        # Set the volume level
        self.media_player.setVolume(volume_level)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec_())