from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from elizaNLP import guess_fruit 
import sys


class BackgroundWidget(QWidget):
    def __init__(self, background_image):
        super().__init__()
        self.background_label = QLabel(self)
        pixmap = QPixmap(background_image)
        self.background_label.setPixmap(pixmap)
        self.background_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fruit Guesser")
       # self.setGeometry(100, 100, 600, 400)
        self.setFixedSize(800, 1000) 

        self.setup_ui()

    def setup_ui(self):
        # Set up the background image
        self.background_label = QLabel(self)
        pixmap = QPixmap("background.png")  
        self.background_label.setPixmap(pixmap)
        self.background_label.setScaledContents(True)
        self.background_label.setGeometry(0, 0, 800, 1000) 

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
        self.start_text1.setStyleSheet("font-size: 36px; font-weight: bold; color: #009688; margin-bottom: 20px")
        self.start_frame_layout.addWidget(self.start_text1)

        # Start button
        self.start_button = QPushButton("Start Game", self.start_frame)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #009688;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
                min-width: 400px;
            }
            QPushButton:hover {
                background-color: #00796B; /* Darken color on hover */
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        self.start_frame_layout.addWidget(self.start_button)

        self.main_layout.addWidget(self.start_frame)

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
        self.chat_box.setFixedHeight(450)  # Set fixed height
        self.chat_box.setFixedWidth(650)  # Set fixed width
        self.chat_box.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ccc; /* Add border */
                border-radius: 10px; /* Rounded corners */
                padding: 5px; /* Add padding */
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #009688; /* Border color on focus */
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
        self.answer_entry.setFixedHeight(100)
        self.answer_entry.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc; /* Add border */
                border-radius: 10px; /* Rounded corners */
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #009688; /* Border color on focus */
            }
            QLineEdit {
                border-bottom: 5px solid rgba(0,0,0,0.1); /* Add shadow */
                border-right: 5px solid rgba(0,0,0,0.1); /* Add shadow */
            }
        """)
        self.chat_layout.addWidget(self.answer_entry)

        self.center_layout.addLayout(self.chat_layout)  # Add chat layout to center layout
        self.game_frame_layout.addLayout(self.center_layout)  # Add center layout to game frame layout

        self.main_layout.addWidget(self.game_frame)

        # Initially hide game frame
        self.game_frame.hide()

    def start_game(self):
        print("Starting the game...")
        self.start_frame.hide()
        self.game_frame.show()

        # Start the fruit guessing game
        self.play_game()

    def play_game(self):
        # Call guess_fruit to get the initial question and additional questions
        self.questions = guess_fruit("")

        # Display initial question
        self.update_output("System", "Think of a fruit and I'll try to guess it! Describe your fruit: ")

        # Hide the answer entry until needed
        self.answer_entry.show()

        # Connect the Enter key to the answer entry
        self.answer_entry.returnPressed.connect(lambda: self.process_response(self.answer_entry.text()))

    def process_response(self, response):
        print("User response:", response)

        # Append the user's response to the chat box
        self.update_output("User", response)

        # Display the next question from the list of questions
        if self.questions:
            next_question = self.questions.pop(0)
            self.update_output("System", next_question)
        else:
            # If there are no more questions, hide the answer entry
            self.answer_entry.hide()

        # Clear the answer entry for the next question
        self.answer_entry.clear()

    def update_output(self, sender, message):
        self.chat_box.append(f"{sender}: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec_())