import streamlit as st
import google.generativeai as genai
import nltk
from nltk.corpus import wordnet
import random

# Configure the API key
genai.configure(api_key='AIzaSyA-14OLSbs0-jwQXc1B9ZYgd1c3bnza9UE')

nltk.download('wordnet')

# Fungsi untuk mendapatkan sinonim kata dari WordNet
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms

# Set default parameters
defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

st.title('Text Correction with Synonyms')
st.write('Enter the text with possible writing mistakes, and I will provide a corrected version along with synonyms.')

# Create a text input for the user's text
user_text = st.text_area("Enter the text:")

# When the 'Correct' button is pressed, generate the corrected text
if st.button('Correct'):
    response = genai.generate_text(
        **defaults,
        prompt=('Correct the following text: ' + user_text)
    )

    # Mendapatkan sinonim untuk setiap kata dalam teks yang diperbaiki
    corrected_text = response.result
    corrected_tokens = corrected_text.split()
    corrected_with_synonyms = []
    for token in corrected_tokens:
        synonyms = get_synonyms(token)
        if synonyms:
            synonym = random.choice(synonyms)
            corrected_with_synonyms.append(f"{token} ({synonym})")
        else:
            corrected_with_synonyms.append(token)

    # Menampilkan teks asli, teks yang diperbaiki, dan sinonim
    st.write("Original Text:")
    st.write(user_text)
    st.write("\nCorrected Text:")
    st.write(corrected_text)
    st.write("\nCorrected Text with Synonyms:")
    st.write(' '.join(corrected_with_synonyms))
