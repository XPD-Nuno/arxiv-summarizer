# arXiv Summarizer

This project searches arXiv using the arXiv API, parses the Atom XML response, and prints a clean report with paper details and a short summary preview.

## Setup
1. Create and activate your Python environment
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Create a .env file based on .env.example

## How to run
Run the interactive app:
python main.py

Run the report module directly:
python summarizer.py

## Example queries
transformer
all:transformer
cs.LG
cat:cs.LG
ti:robot AND cat:cs.RO

## Tests
Run:
python -m pytest -v

## Project structure
config.py manages environment settings
arxiv_api.py fetches raw Atom XML from arXiv
parser.py parses the Atom feed into Python dictionaries
summarizer.py generates a readable report
main.py runs an interactive CLI
test_arxiv.py contains unit tests

## Data source
arXiv API via export.arxiv.org