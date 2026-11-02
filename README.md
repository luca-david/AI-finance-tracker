# Finance Tracker

A terminal-based expense tracker written in Python. Expenses are stored locally in SQLite, and uncategorized ones can be sent to an AI model (Google Gemini) in a single batched request to be categorized automatically.

## Features

- Add, list, view and delete expenses from the command line
- Local storage with SQLite (no server or setup needed)
- AI categorization of all uncategorized expenses in one API call
- Fixed category list, and AI output is validated before it is saved
- Readable tables in the terminal via `rich`

## Tech stack

| Purpose | Library |
|---|---|
| CLI framework | [Typer](https://typer.tiangolo.com/) |
| Terminal output | [Rich](https://rich.readthedocs.io/) |
| Database | `sqlite3` (Python standard library) |
| AI | [google-genai](https://pypi.org/project/google-genai/) (Gemini) |
| Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |

## Requirements

- Python 3.11 or newer
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Setup

```powershell
# 1. Clone the repository and enter it
git clone <your-repo-url>
cd finance-tracker

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1        # macOS/Linux: source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your-key-here
```

The `.env` file and `expenses.db` are listed in `.gitignore` and should never be committed.

## Usage

Run all commands from the project root:

```powershell
python main.py --help
```

| Command | Description |
|---|---|
| `python main.py add "Coffee" 3.5` | Add an expense (date defaults to today) |
| `python main.py add "Train ticket" 12 --date 2026-10-20` | Add an expense with a specific date (YYYY-MM-DD) |
| `python main.py list` | Show all expenses |
| `python main.py list --uncategorized` | Show only expenses without a category |
| `python main.py categorize` | Categorize all uncategorized expenses using AI |

The project also includes commands to delete an expense and to fetch a single expense by its ID. Run `python main.py --help` to see their exact names and options.

### Example

```powershell
python main.py add "Lidl groceries" 45.20
python main.py add "Netflix" 12.99
python main.py add "Bolt ride" 8.50
python main.py categorize
python main.py list
```

## Project structure

```
finance-tracker/
├── main.py              # entry point
├── requirements.txt
├── .env                 # API key (not committed)
├── expenses.db          # SQLite database (created automatically, not committed)
└── expenses/
    ├── __init__.py
    ├── cli.py           # Typer commands
    ├── db.py            # database layer
    └── ai.py            # AI categorization
```

## How the AI categorization works

1. All expenses with no category are collected from the database.
2. Their IDs, descriptions and amounts are sent to Gemini in **one** request, together with the list of allowed categories.
3. The model is asked to reply with JSON in a fixed shape.
4. The response is validated: every ID must be one that was sent, and every category must be in the allowed list. Anything invalid is ignored.
5. Valid categories are written to the database.

Allowed categories: Groceries, Dining, Transport, Housing, Utilities, Entertainment, Health, Shopping, Subscriptions, Travel, Other.

## Privacy note

Expense descriptions and amounts are sent to the AI provider when you run `categorize`. Avoid putting sensitive personal details in descriptions. Free API tiers may use submitted data to improve models, so check the provider's current terms.

## Troubleshooting

- **`GEMINI_API_KEY does not exist inside the .env file`**: the `.env` file is missing, in the wrong folder, or the variable name has a typo.
- **API errors or rate limits**: free tiers have low request limits that can change. Wait and retry, or check your limits in Google AI Studio.
- **`ModuleNotFoundError`**: the virtual environment is not active. Activate it and run `pip install -r requirements.txt`.
