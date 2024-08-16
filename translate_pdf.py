# File path: translate_pdf_to_word.py

import PyPDF2
from deep_translator import GoogleTranslator
from collections import defaultdict
from docx import Document
import time

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    pdf_reader = PyPDF2.PdfReader(open(pdf_path, 'rb'))
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text


# Function to translate each word and create a dictionary with batching and error handling
def translate_words(text, src='en', dest='ar'):
    words = list(set(text.split()))
    dictionary = defaultdict(str)
    
    batch_size = 50  # Number of words to translate in each batch
    for i in range(0, len(words), batch_size):
        batch = words[i:i+batch_size]
        retries = 3  # Number of retries for each batch
        for attempt in range(retries):
            try:
                translations = GoogleTranslator(source=src, target=dest).translate_batch(batch)
                for word, translated in zip(batch, translations):
                    dictionary[word] = translated
                    print(translated)
                break  # Exit the retry loop if successful
            except Exception as e:
                print(f"Error translating batch {i//batch_size + 1}, attempt {attempt + 1}: {e}")
                time.sleep(5)  # Wait before retrying in case of temporary issues
        else:
            # Handle the case where translation fails after all retries
            print(f"Failed to translate batch {i//batch_size + 1} after {retries} attempts.")
    
    return dictionary

# Function to write the dictionary to a Word file in table format
def write_dict_to_word(dictionary, output_word_path):
    document = Document()
    table = document.add_table(rows=1, cols=2)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'English'
    hdr_cells[1].text = 'Arabic'

    for english, arabic in dictionary.items():
        row_cells = table.add_row().cells
        row_cells[0].text = english
        row_cells[1].text = arabic

    document.save(output_word_path)

# Main function to extract, translate, and write to Word
def translate_pdf_to_word(pdf_path, output_word_path):
    # Extract text from the original PDF
    text = extract_text_from_pdf(pdf_path)
    # Translate words and create dictionary
    dictionary = translate_words(text)
    # Write dictionary to Word file
    write_dict_to_word(dictionary, output_word_path)


# Example usage
pdf_path = r'pdf/english_translated.pdf'
output_pdf_path = r'pdf\arabic_translated.docx'
translate_pdf_to_word(pdf_path, output_pdf_path)
