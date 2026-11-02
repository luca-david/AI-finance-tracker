import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv() #reads .env file into environment variables

MODEL = "gemini-3.8-flash"

CATEGORIES = [
    "Groceries", "Dining", "Transport", "Housing", "Utilities",
    "Entertainment", "Health", "Shopping", "Subscriptions", "Travel", "Other",
]

SYSTEM = (
    "You categorize personal expenses. For every expense given, pick exactly one category from the allowed list: "
    f"{', '.join(CATEGORIES)}"
    "If unsure, use 'Other'."
    'Reply with JSON only, in this shape:'
    '{"results": [{"id": 1, "category": "Groceries"}]}'
)

class AIError(Exception):
    """Raised for any problem with the AI step, so the CLI can show a clean message."""

#take all the uncategorized expenses at once as a list, rather than one by one. Minimizes api calls
def categorize(expenses: list[dict]) -> dict[int, str]:
    """Takes [{'id', 'description', 'amount'}, ...] and returns {id: category}."""

    if not expenses:
        return {}
    if not os.getenv("GEMINI_API_KEY"):
        raise AIError("GEMINI_API_KEY does not exist inside the .env file. You need to add it before proceeding")

    lines = "\n".join(
        f"{e['id']}: {e['description']} ({e['amount']:.2f})" for e in expenses
    )

    print(lines)

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])#read from the environment the api
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"Categorize these expenses:\n{lines}",
            config={
                "system_instruction": SYSTEM,
                "response_mime_type": "application/json"
            },
        )
        data = json.loads(response.text)
    except errors.APIError as e:
        raise AIError(f"API call failed: {e}") from e
    except (json.JSONDecodeError, TypeError) as e:
        raise AIError("Model returned invalid JSON") from e

    valid_ids = {e["id"] for e in expenses}
    result: dict[int, str] = {}
    for item in data.get("results", []):
        if item.get("id") in valid_ids and item.get("category") in CATEGORIES:
            result[item["id"]] = item["category"]
    return result