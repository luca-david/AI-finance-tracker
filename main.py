from expenses import db


for row in db.list_expenses():
    expense = dict(row)
    print(f"id: {row["id"]} | description: {row["description"]} | amount: {row["amount"]}")
    print(expense)