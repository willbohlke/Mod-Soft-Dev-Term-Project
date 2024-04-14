import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from functools import partial
import random
from elizaNLP import guess_fruit, analyze_response

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fruit Guesser")
        self.setGeometry(100, 100, 600, 400)

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #333333; color: white;")
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)

        self.start_frame = QWidget(self)
        self.start_frame_layout = QVBoxLayout(self.start_frame)
        self.start_frame_layout.setAlignment(Qt.AlignCenter)

        self.start_text1 = QLabel("Welcome!", self.start_frame)
        self.start_text1.setAlignment(Qt.AlignCenter)
        self.start_text1.setStyleSheet("font-size: 36px; font-weight: bold; color: #009688; margin-bottom: 20px") 
        self.start_frame_layout.addWidget(self.start_text1)

        self.start_text2 = QLabel("Please click the Start Game button to begin the game", self.start_frame)
        self.start_text2.setAlignment(Qt.AlignCenter)
        self.start_text2.setStyleSheet("font-size: 24px;") 
        self.start_frame_layout.addWidget(self.start_text2)

        self.start_button = QPushButton("Start Game", self.start_frame)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #009688;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #00796B; /* Darken color on hover */
            }
        """)
        self.start_button.clicked.connect(self.start_game)
        self.start_frame_layout.addWidget(self.start_button)

        self.game_frame = QWidget(self)
        self.game_frame_layout = QVBoxLayout(self.game_frame)
        self.game_frame_layout.setAlignment(Qt.AlignCenter)

        self.question_label = QLabel(self.game_frame)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("font-size: 18px; color: #009688;")
        self.game_frame_layout.addWidget(self.question_label)

        # Display box for output
        self.output_display = QLabel(self.game_frame)
        self.output_display.setAlignment(Qt.AlignCenter)
        self.output_display.setStyleSheet("font-size: 16px; color: #FFEB3B;")
        self.game_frame_layout.addWidget(self.output_display)

        # Box for user input
        self.answer_entry = QLineEdit(self.game_frame)
        self.answer_entry.setStyleSheet("""
            QLineEdit {
                border: 2px solid #009688;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }
        """)
        self.game_frame_layout.addWidget(self.answer_entry)

        self.main_layout.addWidget(self.start_frame)
        self.main_layout.addWidget(self.game_frame)

        self.game_frame.hide()

    def start_game(self):
        print("Starting the game...")
        self.start_frame.hide()
        self.game_frame.show()

        # Start the fruit guessing game
        self.play_game()

    def play_game(self):
        # Call guess_fruit to get the initial question and additional questions
        initial_question, questions = guess_fruit("")

        # Display initial question
        self.update_output(initial_question)

        # Store the additional questions for later use
        self.questions = questions

        # Hide the answer entry until needed
        self.answer_entry.show()

        # Connect the Enter key to the answer entry
        self.answer_entry.returnPressed.connect(partial(self.next_question, ""))


    def next_question(self, response):
        # Pass the user's response to the backend
        initial_question, questions = guess_fruit(response)  # Pass the response here

        # Update the output with the guess
        self.update_output(initial_question)

        # Clear the answer entry for the next question
        self.answer_entry.clear()

        # If there are no more questions, hide the answer entry
        if not questions:
            self.answer_entry.hide()
            return

        # Remove the current question from the list
        current_question = questions.pop(0)
        # Display the next question
        self.update_output(current_question)
        

    def update_output(self, message):
        self.output_display.setText(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec_())
