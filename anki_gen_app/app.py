import streamlit as st
import os
from file_processor import extract_text_from_pdf, extract_text_from_txt, chunk_text, split_by_chapters
from llm_client import generate_anki_cards
from anki_generator import create_anki_deck

st.set_page_config(page_title="AI Anki Card Generator", layout="wide")

st.title("🤖 AI Anki Card Generator")
st.markdown("""
Upload a PDF or TXT file, provide a prompt, and let AI generate Anki cards for you!
Support for **MathJax** (LaTeX) is included. Large files are automatically split into chunks.
""")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.info("You can get an API key from [Google AI Studio](https://aistudio.google.com/).")

    st.subheader("Deck Settings")
    deck_name_input = st.text_input("Deck Name", value="AI Generated Deck")

    st.subheader("Advanced Settings")
    chunk_size = st.number_input("Chunk Size (characters)", min_value=1000, max_value=100000, value=20000, step=1000)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload File")
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'])

    st.subheader("2. Custom Instructions")
    user_prompt = st.text_area(
        "Describe how you want the cards to look",
        placeholder="Example: Create cards for all definitions. Use simple language. Focus on the mathematical proofs...",
        height=150
    )

if uploaded_file and api_key:
    if st.button("Generate Cards", type="primary"):
        with st.spinner("Reading file..."):
            try:
                # 1. Extract Text
                text_content = ""
                if uploaded_file.type == "application/pdf":
                    text_content = extract_text_from_pdf(uploaded_file)
                else:
                    text_content = extract_text_from_txt(uploaded_file)

                if not text_content:
                    st.error("Could not extract text from the file.")
                    st.stop()

                st.success(f"Successfully extracted {len(text_content)} characters.")

                # 2. Split by Chapters and then Chunk if necessary
                chapters = split_by_chapters(text_content)
                
                all_processing_units = []
                for chap in chapters:
                    chap_title = chap['title']
                    chap_content = chap['content']
                    
                    if len(chap_content) > chunk_size:
                        # If chapter is too big, chunk it but keep the title context
                        sub_chunks = chunk_text(chap_content, chunk_size=chunk_size)
                        for j, sc in enumerate(sub_chunks):
                            all_processing_units.append({
                                'display_name': f"{chap_title} (Part {j+1})",
                                'content': sc
                            })
                    else:
                        all_processing_units.append({
                            'display_name': chap_title,
                            'content': chap_content
                        })

                st.info(f"Split document into {len(all_processing_units)} sections based on chapters.")

                # 3. Process Units
                all_cards = []
                progress_bar = st.progress(0)

                for i, unit in enumerate(all_processing_units):
                    # Update progress
                    progress = (i + 1) / len(all_processing_units)
                    progress_bar.progress(progress, text=f"Processing: {unit['display_name']}...")

                    # Call LLM
                    chunk_cards = generate_anki_cards(api_key, unit['content'], user_prompt)
                    if chunk_cards:
                        all_cards.extend(chunk_cards)

                if not all_cards:
                    st.error("Failed to generate cards. The AI might have returned an invalid response or there was an API error.")
                else:
                    st.success(f"Generated {len(all_cards)} cards in total!")

                    # Preview Cards
                    with st.expander("Preview Generated Cards"):
                        for i, card in enumerate(all_cards):
                            st.markdown(f"**Card {i+1}**")
                            st.markdown(f"**Front:** {card['front']}")
                            st.markdown(f"**Back:** {card['back']}")
                            st.divider()

                    # 4. Create Anki Deck
                    output_filename = create_anki_deck(all_cards, deck_name=deck_name_input)

                    # 5. Download Button
                    with open(output_filename, "rb") as f:
                        file_bytes = f.read()

                    st.download_button(
                        label="Download .apkg Deck",
                        data=file_bytes,
                        file_name=f"{deck_name_input.replace(' ', '_').lower()}.apkg",
                        mime="application/octet-stream"
                    )

                    # Clean up
                    os.remove(output_filename)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif not api_key:
    st.warning("Please enter your Google Gemini API Key in the sidebar to proceed.")
