import sqlite3
from contextlib import closing
from datetime import date

DB_PATH = "expenses.db"

def get_conn() -> sqlite3.Connection:
    #sqlite is synchronous, thus the code is executed sequentially without the need for promises or await
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #rows behave like dicts
    return conn

def init_db() -> None: #function returns None
    # "with" blocks act like "try/finally" with automatic cleanup
    with closing(get_conn()) as conn, conn:
        conn.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        description TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL,
                        category TEXT
                    )
                """)

def add_expense(description: str, amount: float, on: str | None = None) -> int:
    on = on or date.today().isoformat()
    with closing(get_conn()) as conn, conn:
        cur = conn.execute(
            #use "?" to avoid SQL injection
            "INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)",
            (description, amount, on),
        )
        return cur.lastrowid

def list_expenses(only_uncategorized: bool = False) -> list[sqlite3.Row]: #returns an array of DB rows
    query = "SELECT * FROM expenses"
    if only_uncategorized:
        query += " WHERE category IS NULL"
    query += " ORDER BY date DESC, id DESC"
    with closing(get_conn()) as conn, conn:
        result = conn.execute(query).fetchall()
        return result

#sets the category of an expense
def set_category(expense_id: int, category: str) -> None:
    with closing(get_conn()) as conn, conn:
        conn.execute(
            "UPDATE expenses SET category = ? WHERE id = ?", (category, expense_id)
        )

def get_last_expense() -> sqlite3.Row:
    query = "SELECT * FROM expenses ORDER BY id DESC"
    with closing(get_conn()) as conn, conn:
        result = conn.execute(query).fetchone()
        return result