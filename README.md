# AI Anki Card Generator

A small Streamlit application that turns PDF and text material into an Anki
deck (`.apkg`) with Google Gemini. It is designed for study workflows: upload
one or more documents, choose instructions for the cards, review the generated
front/back pairs, and download a deck that can be imported into Anki.

## What it demonstrates

- PDF and plain-text extraction
- Chapter-aware splitting and size-bounded chunking for larger documents
- LLM-assisted flashcard generation with custom instructions
- Anki deck creation via `genanki`
- A straightforward Streamlit interface with multi-file upload and preview

## Run locally

Requires Python 3.10+ and a Google Gemini API key.

```bash
cd anki_gen_app
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Enter the API key in the app's sidebar; it is not stored by the application.

## Tests

```bash
cd anki_gen_app
python -m unittest discover -p 'test_*.py'
```

## Privacy

Uploaded text is sent to the configured Gemini API to generate cards. Do not
upload material that you are not permitted to share with that service.
