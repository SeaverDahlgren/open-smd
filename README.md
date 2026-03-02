# Minimal Terminal Chatbot

This project is a basic chatbot you can run in your terminal.

## Requirements

- Python 3.8+
- `GEMINI_API_KEY`
- `certifi` package (`pip install certifi`)

## Success Criteria Coverage

- Interactive shell: user enters commands in the terminal prompt.
- Chatbot output: assistant responses are printed back to terminal.
- Context across turns: previous user/assistant turns are retained and sent with each new request.

## Setup

1. Create and activate a virtual environment (recommended):
   - `python3 -m venv .venv`
   - `source .venv/bin/activate`
2. Set your API key:
   - `export GEMINI_API_KEY="your_key_here"`
3. Optional: choose a model (default is `gemini-2.5-flash`):
   - `export GEMINI_MODEL="gemini-2.5-flash"`

## Run

`python3 chatbot.py`

Press Keyboard Interrupt (CTRL+C) to stop.

