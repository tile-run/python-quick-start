# Tile API Python Quick Start

Extract data from unstructured files (PDFs, images, text) using Tile's API. Get your API key by signing up for an account at https://tile.run.

## Setup

1. Clone this repository
2. Create virtual environment:
   ```bash
   python -m venv .
   source bin/activate  # On Mac/Linux
   # or
   Scripts\activate     # On Windows
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Copy your .env.example file and save it as .env. Update the value for the API key.
5. Update the `file_path` to the file you want to use. Remember to change the content_type for the reuqest.
6. Run: `python main.py`
