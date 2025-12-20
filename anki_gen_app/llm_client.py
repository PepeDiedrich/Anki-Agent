import google.generativeai as genai
import json
import os

def generate_anki_cards(api_key, text_content, user_prompt=""):
    """
    Sends the text content and user prompt to Gemini to generate Anki cards.
    Returns a list of dictionaries [{'front': '...', 'back': '...'}].
    """
    genai.configure(api_key=api_key)

    # We use a model capable of JSON mode or just good instruction following.
    model = genai.GenerativeModel('gemini-1.5-flash')

    base_prompt = """
    You are an expert at creating Anki flashcards.
    Your task is to extract key concepts, definitions, and questions from the provided text and format them as a JSON list of objects.
    Each object must have exactly two keys: "front" (the question or term) and "back" (the answer or definition).

    IMPORTANT REQUIREMENTS:
    1. Output MUST be a valid JSON array. Do not include markdown code blocks (like ```json ... ```) in the output, just the raw JSON string.
    2. For mathematical formulas, use standard LaTeX syntax compatible with MathJax.
       - Use \\( ... \\) for inline math.
       - Use \\[ ... \\] for block math.
       - Example: "The area of a circle is \\( A = \\pi r^2 \\)."
    3. Create comprehensive cards that cover the material well.
    4. If the user provided specific instructions below, prioritize them.
    5. If the text seems to be a fragment or cut off, just process what you have to the best of your ability.

    User Instructions:
    {user_instruction}

    Content to process:
    {content}
    """

    # We no longer truncate here, trusting the caller to handle chunking if needed,
    # though 1.5 Flash has a massive context window so it's quite safe.
    formatted_prompt = base_prompt.format(
        user_instruction=user_prompt if user_prompt else "No specific additional instructions.",
        content=text_content
    )

    try:
        # Increase token limit for response if needed, though default is usually fine for a list of cards
        response = model.generate_content(formatted_prompt)
        response_text = response.text.strip()

        # Clean up if the model wraps in markdown
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        cards = json.loads(response_text)

        # Validate structure
        valid_cards = []
        if isinstance(cards, list):
            for card in cards:
                if 'front' in card and 'back' in card:
                    valid_cards.append(card)
        else:
            print("Warning: Model did not return a list.")

        return valid_cards

    except json.JSONDecodeError:
        # Fallback or error handling if JSON is malformed
        print("Error: content was not valid JSON.")
        print("Raw response:", response_text)
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
