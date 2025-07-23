import fitz  # PyMuPDF
import os
import json

# Define the input and output directories relative to the script's location
# ../input/ tells the script to go one level up and then into the 'input' folder.
INPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'input')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a given PDF file."""
    try:
        # Open the PDF file
        doc = fitz.open(pdf_path)
        full_text = ""
        # Iterate through each page and extract text
        for page in doc:
            full_text += page.get_text()
        doc.close()
        return full_text
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def process_all_pdfs():
    """Processes all PDF files in the input directory."""
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Searching for PDFs in: {INPUT_DIR}")

    # Loop through all files in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}...")

            # 1. Extract text
            extracted_text = extract_text_from_pdf(pdf_path)

            if extracted_text:
                # 2. Create the JSON structure
                output_data = {
                    "source_file": filename,
                    "extracted_text": extracted_text.strip()
                }

                # 3. Save the JSON output file
                json_filename = os.path.splitext(filename)[0] + '.json'
                json_path = os.path.join(OUTPUT_DIR, json_filename)

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=4, ensure_ascii=False)

                print(f"Successfully created {json_filename} in {OUTPUT_DIR}")

if __name__ == "__main__":
    process_all_pdfs()
    print("\n✅ All PDFs have been processed!")