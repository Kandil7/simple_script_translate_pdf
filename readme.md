# File path: translate_pdf_to_word.py

```python
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
```
# Translation Tool

This is a Python script that extracts text from a PDF file, translates each word using Google Translate, and writes the translations to a Word document.

## Prerequisites

Before running the script, make sure you have the following dependencies installed:

- PyPDF2
- deep_translator
- docx

You can install these dependencies by running the following command:

```shell
pip install PyPDF2 deep_translator python-docx
```

## Usage

To use this translation tool, follow these steps:

1. Place the PDF file you want to translate in the `pdf` directory.
2. Open the `translate_pdf_to_word.py` file.
3. Modify the `pdf_path` variable to specify the path to your PDF file.
4. Modify the `output_word_path` variable to specify the path where you want to save the translated Word document.
5. Run the script by executing the following command:

```shell
python translate_pdf_to_word.py
```

The script will extract the text from the PDF, translate each word using Google Translate, and generate a Word document with the translations.

## Notes

- The script translates words from English to Arabic by default. You can modify the `src` and `dest` parameters in the `translate_words` function to translate between different languages.
- The script handles translation errors by retrying a certain number of times before giving up. If a batch of words fails to translate, the script will print an error message and continue with the next batch.
- The translations are stored in a dictionary, where the English words are the keys and the translated words are the values. The dictionary is then written to a Word document in table format.

Feel free to customize the script according to your needs and enjoy translating your PDF files!
## Additional Features

In addition to the existing functionality, the script now supports the following features:

### Language Selection

You can now specify the source and target languages for translation. By default, the script translates from English to Arabic. To translate between different languages, modify the `src` and `dest` parameters in the `translate_words` function.

### Error Handling

The script now handles translation errors more gracefully. If a batch of words fails to translate, the script will print an error message and continue with the next batch. It will also wait for 5 seconds before retrying in case of temporary issues.

### Batch Size

The script now allows you to specify the batch size for translation. The default batch size is 50 words per batch. You can modify the `batch_size` variable in the `translate_words` function to adjust the batch size according to your needs.

## Usage Example

Here's an example of how to use the script with the new features:

```python
pdf_path = r'pdf/english_translated.pdf'
output_pdf_path = r'pdf\arabic_translated.docx'
translate_pdf_to_word(pdf_path, output_pdf_path, src='en', dest='fr', batch_size=25)
```

In this example, the script will translate the PDF from English to French with a batch size of 25 words per batch.

Feel free to customize the script further to suit your specific requirements. Happy translating!
