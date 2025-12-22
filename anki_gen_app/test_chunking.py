import unittest
from file_processor import chunk_text, split_by_chapters

class TestChunker(unittest.TestCase):
    def test_chunking_basic(self):
        text = "a" * 100
        # Chunk size 20, overlap 5. Should produce roughly 100/15 chunks approx.
        chunks = chunk_text(text, chunk_size=20, overlap=5)

        # Concatenate chunks roughly checks we have coverage (ignoring overlap duplication)
        self.assertTrue(len(chunks) > 1)
        self.assertTrue(all(len(c) <= 20 for c in chunks))

    def test_chunking_with_newlines(self):
        # Create text with sentences
        sentences = [f"Sentence {i}." for i in range(10)]
        text = "\n".join(sentences)

        # Chunk small enough to force split
        chunks = chunk_text(text, chunk_size=30, overlap=5)

        self.assertTrue(len(chunks) > 1)
        # Check that we didn't lose content (naive check: last chunk ends with last sentence)
        self.assertTrue(chunks[-1].strip().endswith("Sentence 9."))

    def test_split_by_chapters(self):
        text = """
Kapitel 1: Einleitung
Dies ist der Inhalt von Kapitel 1.
Es geht um Grundlagen.

Kapitel 2: Fortgeschrittene Themen
Hier wird es komplizierter.
Mehr Details folgen.

3. Zusammenfassung
Das war's.
"""
        chapters = split_by_chapters(text)
        self.assertEqual(len(chapters), 3)
        self.assertEqual(chapters[0]['title'], "Kapitel 1: Einleitung")
        self.assertEqual(chapters[1]['title'], "Kapitel 2: Fortgeschrittene Themen")
        self.assertEqual(chapters[2]['title'], "3. Zusammenfassung")
        self.assertIn("Grundlagen", chapters[0]['content'])
        self.assertIn("komplizierter", chapters[1]['content'])
        self.assertIn("Das war's", chapters[2]['content'])

if __name__ == '__main__':
    unittest.main()
