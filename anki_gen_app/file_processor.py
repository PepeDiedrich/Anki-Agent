import io
from pypdf import PdfReader

def extract_text_from_txt(file_obj) -> str:
    """Reads text from a TXT file object."""
    try:
        content = file_obj.read().decode("utf-8")
        return content
    except Exception as e:
        raise ValueError(f"Error reading TXT file: {e}")

def extract_text_from_pdf(file_obj) -> str:
    """Extracts text from a PDF file object."""
    try:
        reader = PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")

def chunk_text(text: str, chunk_size: int = 20000, overlap: int = 1000) -> list[str]:
    """
    Splits text into chunks of approximately `chunk_size` characters.
    Includes an `overlap` to ensure context isn't lost at boundaries.
    """
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size

        # If we are not at the end of the text, try to find a nice break point (newline or period)
        if end < text_len:
            # Look for the last newline in the potential chunk to break cleanly
            # We look in the last 10% of the chunk to avoid making it too small
            search_start = max(start, end - int(chunk_size * 0.1))
            last_newline = text.rfind('\n', search_start, end)

            if last_newline != -1:
                end = last_newline + 1
            else:
                # If no newline, look for a period
                last_period = text.rfind('. ', search_start, end)
                if last_period != -1:
                    end = last_period + 2

        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward, subtracting overlap, but ensure we don't get stuck
        start = end - overlap

        # Special case: if overlap pushes us back behind or to current start, forced forward to avoid infinite loop
        if start < end - chunk_size: # Should not happen with valid inputs
             start = end

        # If we reached the end, break
        if end >= text_len:
            break

    return chunks
