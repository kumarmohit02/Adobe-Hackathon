import fitz  # PyMuPDF
import os
import json
import re

# Define the input and output directories
INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

def is_heading(block_text):
    """
    A simple heuristic to determine if a text block is a heading.
    - It should not end with a period.
    - It should be relatively short (e.g., less than 15 words).
    - It often uses Title Case.
    """
    block_text = block_text.strip()
    if not block_text:
        return False
    
    # Rule 1: Doesn't end with a period.
    if block_text.endswith('.'):
        return False
        
    # Rule 2: Word count is low.
    if len(block_text.split()) > 15:
        return False
        
    # Rule 3: A high percentage of words are capitalized (common in titles)
    words = block_text.split()
    capitalized_words = sum(1 for word in words if word.istitle() or word.isupper())
    if capitalized_words / len(words) < 0.5:
         return False

    return True

def clean_and_deduplicate(text):
    """
    Cleans up a paragraph by removing extra whitespace
    and deduplicating repeated sentences.
    """
    # Split into sentences, preserving sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text.replace('\n', ' ').strip())
    
    # Use a set to keep only unique sentences, preserving order
    unique_sentences = list(dict.fromkeys(sentences))
    
    return ' '.join(unique_sentences)


def process_pdf_structurally(pdf_path):
    """
    Processes a PDF to extract a structured list of headings and paragraphs.
    """
    try:
        doc = fitz.open(pdf_path)
        structured_content = []
        
        for page in doc:
            # Extract text as blocks, which often correspond to paragraphs or elements
            blocks = page.get_text("blocks")
            for block in blocks:
                # block[4] contains the text content
                raw_text = block[4].strip()
                if not raw_text:
                    continue

                if is_heading(raw_text):
                    # Clean up any repeated heading text
                    cleaned_text = clean_and_deduplicate(raw_text)
                    structured_content.append({"type": "heading", "text": cleaned_text})
                else:
                    # Clean up paragraph text
                    cleaned_text = clean_and_deduplicate(raw_text)
                    # Avoid adding empty or tiny paragraphs
                    if len(cleaned_text) > 10:
                        # If the last item was a paragraph, append to it.
                        # This helps merge paragraphs that were split into separate blocks.
                        if (structured_content and 
                            structured_content[-1]["type"] == "paragraph"):
                            structured_content[-1]["text"] += " " + cleaned_text
                        else:
                            structured_content.append({"type": "paragraph", "text": cleaned_text})

        doc.close()
        return structured_content
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def process_all_pdfs_b():
    """Processes all PDF files for Round 1B."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Searching for PDFs in: {INPUT_DIR}")
    
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing (Round 1B): {filename}...")
            
            structured_data = process_pdf_structurally(pdf_path)
            
            if structured_data:
                # We will name the output file with a "_b" suffix
                json_filename = os.path.splitext(filename)[0] + '_structured.json'
                json_path = os.path.join(OUTPUT_DIR, json_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(structured_data, f, indent=4, ensure_ascii=False)
                    
                print(f"Successfully created structured file {json_filename}")

if __name__ == "__main__":
    process_all_pdfs_b()
    print("\n✅ All PDFs have been processed for Round 1B!")