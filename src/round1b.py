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
    """
    block_text = block_text.strip()
    if not block_text:
        return False
    
    if block_text.endswith('.'):
        return False
        
    if len(block_text.split()) > 15:
        return False
        
    words = block_text.split()
    if not words: return False
    capitalized_words = sum(1 for word in words if word.istitle() or word.isupper())
    if capitalized_words / len(words) < 0.5:
         return False

    return True

def clean_and_deduplicate(text):
    """
    Cleans up a paragraph by removing extra whitespace
    and deduplicating repeated sentences.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.replace('\n', ' ').strip())
    unique_sentences = list(dict.fromkeys(s.strip() for s in sentences if s))
    return ' '.join(unique_sentences)

def process_pdf_structurally(pdf_path):
    """
    Processes a PDF to extract an intermediate list of headings and paragraphs.
    """
    try:
        doc = fitz.open(pdf_path)
        structured_content = []
        
        for page in doc:
            blocks = page.get_text("blocks")
            for block in blocks:
                raw_text = block[4].strip()
                if not raw_text:
                    continue

                cleaned_text = clean_and_deduplicate(raw_text)
                if not cleaned_text:
                    continue

                if is_heading(cleaned_text):
                    structured_content.append({"type": "heading", "text": cleaned_text})
                else:
                    if (structured_content and 
                        structured_content[-1]["type"] == "paragraph"):
                        # Merge with the previous paragraph if it was also a paragraph
                        structured_content[-1]["text"] += " " + cleaned_text
                    else:
                        structured_content.append({"type": "paragraph", "text": cleaned_text})

        doc.close()
        return structured_content
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def format_with_sequential_keys(structured_list):
    """
    Transforms the intermediate list into the final dictionary
    with h1, p1, h2, etc., keys.
    """
    final_dict = {}
    heading_counter = 1
    paragraph_counter = 1
    for item in structured_list:
        if item["type"] == "heading":
            key = f"h{heading_counter}"
            final_dict[key] = item["text"]
            heading_counter += 1
        elif item["type"] == "paragraph":
            key = f"p{paragraph_counter}"
            final_dict[key] = item["text"]
            paragraph_counter += 1
    return final_dict

def process_all_pdfs_b():
    """Processes all PDF files for Round 1B."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Searching for PDFs in: {INPUT_DIR}")
    
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing (Round 1B): {filename}...")
            
            # 1. Get the intermediate list of headings and paragraphs
            intermediate_list = process_pdf_structurally(pdf_path)
            
            if intermediate_list:
                # 2. Transform the list into the final dictionary format
                final_output_dict = format_with_sequential_keys(intermediate_list)

                # 3. Save the final dictionary to a JSON file
                json_filename = os.path.splitext(filename)[0] + '_structured.json'
                json_path = os.path.join(OUTPUT_DIR, json_filename)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(final_output_dict, f, indent=4, ensure_ascii=False)
                    
                print(f"Successfully created structured file {json_filename}")

if __name__ == "__main__":
    process_all_pdfs_b()
    print("\n✅ All PDFs have been processed for Round 1B!")