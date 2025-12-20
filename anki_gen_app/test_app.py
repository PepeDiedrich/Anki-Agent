import unittest
import io
import os
from file_processor import extract_text_from_txt
from anki_generator import create_anki_deck

class TestAnkiGenApp(unittest.TestCase):

    def test_extract_text_from_txt(self):
        # Create a dummy BytesIO object simulating a file upload
        content = b"Hello World"
        file_obj = io.BytesIO(content)
        text = extract_text_from_txt(file_obj)
        self.assertEqual(text, "Hello World")

    def test_anki_deck_creation(self):
        # Dummy data
        cards = [
            {"front": "Question 1", "back": "Answer 1"},
            {"front": "Math Question", "back": r"\( x^2 \)"}
        ]
        filename = create_anki_deck(cards, "Test Deck")

        # Check if file exists
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(os.path.getsize(filename) > 0)

        # Cleanup
        os.remove(filename)

if __name__ == '__main__':
    unittest.main()
