import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation


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
        self.start_text1.setStyleSheet("font-size: 30px;") 
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
                border: 2px solid #009688;
                border-radius: 10px;
                padding: 10px 20px;
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
        self.start_frame.hide()
        self.game_frame.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.showMaximized()  # Show window in fullscreen mode
    sys.exit(app.exec())
