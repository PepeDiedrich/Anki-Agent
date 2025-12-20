import genanki
import random
import time

# Define a simple Anki model with MathJax support
# Note: Modern Anki versions have built-in MathJax support.
# We include standard LaTeX delimiters in the template just in case, or rely on the content having them.

MODEL_ID = 1607392319

def get_math_model():
    """
    Returns a genanki Model that supports basic Front/Back cards with CSS for styling.
    """
    return genanki.Model(
        MODEL_ID,
        'Simple Math Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div class="card">{{Question}}</div>',
                'afmt': '{{FrontSide}}<hr id="answer"><div class="card">{{Answer}}</div>',
            },
        ],
        css="""
        .card {
            font-family: arial;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }
        """
    )

def create_anki_deck(cards_data, deck_name="Generated Deck"):
    """
    Creates an Anki deck from a list of dictionaries [{'front': '...', 'back': '...'}].
    Returns the path to the generated .apkg file.
    """
    # Generate a unique DECK_ID based on current time to avoid conflicts
    # Anki uses a 32-bit integer for deck IDs (signed in some contexts, so keeping it safe)
    # Using random combined with time to ensure uniqueness
    deck_id = int(time.time() * 1000) % (1 << 31)

    deck = genanki.Deck(deck_id, deck_name)
    model = get_math_model()

    for card in cards_data:
        note = genanki.Note(
            model=model,
            fields=[card['front'], card['back']]
        )
        deck.add_note(note)

    # Generate a random output filename to avoid collisions if running concurrently (though locally it's fine)
    output_filename = f"anki_deck_{random.randint(1000, 9999)}.apkg"
    genanki.Package(deck).write_to_file(output_filename)
    return output_filename
