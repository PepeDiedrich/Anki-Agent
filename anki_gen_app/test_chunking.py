import unittest
from file_processor import chunk_text

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

if __name__ == '__main__':
    unittest.main()
