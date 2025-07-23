
# PDF Structure Extractor

A robust Python application designed for an Adobe Hackathon to parse PDF documents, intelligently extract structured content like headings and paragraphs, and serialize the output into clean JSON format.

## Table of Contents

  - [About The Project]
  - [Features]
  - [Technology Stack]
  - [Getting Started]
  - [Prerequisites]
  - [Installation]
  - [Usage]
  - [Running with Docker]
  - [License]
 
## About The Project

This project addresses the common challenge of extracting meaningful information from unstructured PDF files. Standard text extraction often results in a single, unformatted block of text, losing the document's inherent structure. This solution not only extracts text but also intelligently identifies and separates structural elements like headings and paragraphs, providing a clean, machine-readable JSON output.

## Features

  - **Raw Text Extraction**: Pulls all text content from PDF files.
  - **Structural Analysis**: Intelligently identifies headings vs. paragraphs using heuristics.
  - **Text Deduplication**: Cleans the output by removing repeated sentences within a paragraph.
  - **JSON Output**: Saves the structured data in a clean, easy-to-use JSON format.
  - **Dockerized**: Fully containerized with a `Dockerfile` for easy deployment and scalability.

## Technology Stack

  - **[Python 3.9](https://www.python.org/)**: The core programming language.
  - **[PyMuPDF (fitz)](https://github.com/pymupdf/PyMuPDF)**: A high-performance Python library for PDF processing.
  - **[Docker](https://www.docker.com/)**: For containerization and reproducible builds.

## Getting Started

Follow these instructions to set up the project on your local machine.

### Prerequisites

Ensure you have the following installed:

  - Python 3.9 or higher
  - pip (Python package installer)

### Installation

1.  **Clone the repository (or download the source code):**
    ```sh
    git clone https://your-repository-url.com
    cd project-folder
    ```
2.  **Create and activate a virtual environment:**
    ```sh
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Install the required packages:**
    ```sh
    pip install -r src/requirements.txt
    ```

## Usage

1.  **Add PDF Files**: Place the PDF files you want to process into the `/input` directory.

2.  **Execute the script**: To run the structural analysis and generate the final JSON output, run `round1b.py` from the project's root directory.

    ```sh
    python src/round1b.py
    ```

3.  **Check the Output**: The resulting structured JSON files will be created in the `/output` directory.

##  Running with Docker

For a more isolated and reproducible setup, you can use the provided `Dockerfile`.

1.  **Prerequisite**: Docker must be installed and running on your system.

2.  **Build the Docker image:**
    From the root of the project directory, run:

    ```sh
    docker build -t adobe-hackathon-extractor .
    ```

3.  **Run the Docker container:**
    This command mounts your local `input` and `output` folders to the container, so it can read your PDFs and write the JSON files back to your machine.

    ```sh
    docker run --rm \
      -v "$(pwd)/input:/app/input" \
      -v "$(pwd)/output:/app/output" \
      adobe-hackathon-extractor
    ```

    The processed files will appear in your `/output` folder as soon as the container finishes its run.

## 📄 License

This project is distributed under the MIT License. See `LICENSE` file for more information.
