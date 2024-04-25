import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QLineEdit, QTextBrowser

from Similarity import Similarity  # You'll need to have the Similarity implementation
from ELIZA_logic import ELIZAGame
from gui import WorkerThread, InteractivePromptGUI


class TestELIZAGame(unittest.TestCase):

    def setUp(self):
        self.game = ELIZAGame()
        # Patch os.listdir to control test environment
        self.mock_listdir = patch('os.listdir').start()
        self.mock_listdir.return_value = ['animals.txt', 'colors.txt']

    def tearDown(self):
        patch.stopall()  # Stop all patches

    def test_start_game_valid(self):
        result = self.game.start_game()
        self.assertIn("Welcome to the ELIZA Guess Bot", result)
        self.assertIn("book", result)

    def test_select_game_mode_valid(self):
        result = self.game.select_game_mode('book')
        self.assertEqual(result, "Category selected. Describe the book you're thinking of.")
        self.assertEqual(self.game.object_type, "book.txt")
        self.assertIsNotNone(self.game.similarity)

    def test_select_game_mode_invalid(self):
        result = self.game.select_game_mode('invalid')
        self.assertEqual(result, "Invalid selection. Please select a valid category.")

    def test_play_error_not_initialized(self):
        self.game.similarity = None  # Simulate not initialized
        result = self.game.play("test description")
        self.assertEqual(result, "> Error: Game mode not properly initialized or similarity object not created.")

    @patch('os.path.join')
    @patch('builtins.open')
    def test_play_with_guesses(self, mock_open, mock_os_join):
        mock_similarity = MagicMock(Similarity)
        mock_similarity.get_guesses.return_value = ('strong', [('dog', 0.9)])
        self.game.similarity = mock_similarity

        result = self.game.play("It's furry and has four legs")

        # Assert that the thinking animation runs temporarily
        self.assertIsNotNone(self.game.thinking_timer)
        # Ensure threading and getting guesses is initiated
        mock_similarity.get_guesses.assert_called_with("It's furry and has four legs ")
        self.assertTrue(self.game.guesses_ready.is_set())
        # Check correct output
        self.assertEqual(result, "Is it dog?")

class SimilarityTests(unittest.TestCase):

    def setUp(self):
        self.similarity = Similarity(["Example Object 1", "Example Object 2"], "Movie")  # Set up Similarity object


    def test_lemmatize_text(self):
        input_text = "The cats were running."
        expected_output = "the cat be run ."
        lemmatized_text = self.similarity.lemmatize_text(input_text)
        self.assertEqual(lemmatized_text, expected_output)

class TestWorkerThread(unittest.TestCase):
    def test_operation_done_signal(self):
        game = MagicMock()  # Simple mock for the game object
        thread = WorkerThread("", game)
        result = ""

        def set_result(output):
            nonlocal result
            result = output

        thread.operation_done.connect(set_result)
        thread.start()
        thread.wait()  # Wait for the thread to finish

        self.assertEqual(result, "")  # Or any expected output you set in your mock

class TestInteractivePromptGUI(unittest.TestCase):
    @patch('PyQt5.QtGui.QImage')  # Patch loading of the background image
    def test_init_ui(self, mock_image):
        gui = InteractivePromptGUI()
        # Assertions to check if UI elements are created, etc.
        self.assertIsInstance(gui.text_browser, QTextBrowser)
        self.assertIsInstance(gui.line_edit, QLineEdit)

    def test_start_game(self):
        gui = InteractivePromptGUI()
        game_mock = MagicMock()
        game_mock.start_game.return_value = "Welcome to ELIZA!"
        gui.game = game_mock  # Inject the mock

        gui.start_game()

        # Assert the text browser is updated with the welcome message
        self.assertEqual(gui.text_browser.toPlainText(), "Welcome to ELIZA!")

