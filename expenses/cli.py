from datetime import date as date_type
from rich.console import Console
from rich.table import Table

from expenses import db

import typer

app = typer.Typer(help="Track expenses and categorize them with AI")
console = Console()

@app.callback()
def main() -> None:
    """Runs before every command"""
    db.init_db()

@app.command()
def add(description: str, amount: float, date: str | None = None) -> None:
    """Add an expense. Date (YYYY-MM-DD) is optional, defaults to today's date"""
    if date:
        try:
            date_type.fromisoformat(date)
        except ValueError:
            raise typer.BadParameter("Use YYYY-MM-DD format", param_hint="--date")
    expense_id = db.add_expense(description, amount, date)
    console.print(f"[green]Added[/green] #{expense_id}: {description} ({amount:.2f})")

@app.command("all")
def list_expenses(uncategorized: bool = False) -> None:
    """Show all expenses"""
    rows = db.list_expenses(only_uncategorized=uncategorized)
    if not rows:
        console.print("[yellow]No expenses yet[/yellow]")
        return
    table = Table("ID", "Description", "Amount", "Category", "Date")
    for row in rows:
        table.add_row(
            str(row["id"]), row["description"], str(row["amount"]), row["category"] or "-", row["date"]
        )
    console.print("[green]All expenses[/green]")
    console.print(table)

@app.command("last")
def show_last_expense() -> None:
    """Get the last tracked expense"""
    row = db.get_last_expense()
    if not row:
        console.print("[red]No expenses yet[/red]")
        return
    table = Table("ID", "Description", "Amount", "Category", "Date")
    table.add_row(str(row["id"]), row["description"], str(row["amount"]), row["category"] or "-", row["date"])
    console.print("[blue]Last expense[/blue]")
    console.print(table)

@app.command("on-id")
def show_expense_on_id(expense_id: int) -> None:
    """Search for an expense in the database based on its id"""
    # no check for id needed,typer handles checks automatically
    row = db.get_expense_on_id(expense_id)
    if not row:
        console.print("[red]No expense exists for the given id[/red]")
        return
    table = Table("ID", "Description", "Amount", "Category", "Date")
    table.add_row(str(row["id"]), row["description"], str(row["amount"]), row["category"] or "-", row["date"])
    console.print("Searched for expense with id " + str(expense_id))
    console.print(table)

