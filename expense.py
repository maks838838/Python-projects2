import json
import csv
import argparse
from datetime import datetime

def id_check(expenseslist):
    expected_id = 1
    for expense in expenseslist:    
        if expense["id"] != expected_id:
            expense["id"] = expected_id
        expected_id += 1
def savetofile(expenseslist):
    id_check(expenseslist)
    with open("expenses.json", "w") as file:
        json.dump(expenseslist, file, indent=4)
def printlist(expenseslist):
    print("expenses:")
    if len(expenseslist) == 0: 
        print("you have no expenses")
        return
    id_check(expenseslist)
    for expense in expenseslist:
        print(f'{expense["id"]}. {expense["description"]}, {expense["amount"]}, ({expense["category"]})', expense["date"], expense["date_u"])
def add_expense(expenseslist, args):
    if args.description.strip() == "":
        print("Description cannot be empty.")
        return
    if args.amount < 0:
        print("u can not add negative amount")
        return    
    if len(expenseslist) == 0:
            expense_id = 1
    else:
        expense_id = expenseslist[-1]["id"]+1
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_expense = {"id": expense_id, "amount": args.amount, "description": args.description, "category": args.type, "date": time, "date_u":"No changes"}
    expenseslist.append(new_expense)
    printlist(expenseslist)
    savetofile(expenseslist)
def delete_expense(expenseslist, args):         
    found = False
    for expense in expenseslist:
        if args.id == expense["id"]:
            found = True
            expenseslist.remove(expense)
            break
    if not found:    
        print("no expense with this id")
        return
    printlist(expenseslist)
    print(args.id, "expense was deleted")
    savetofile(expenseslist)
def update_expense(expenseslist, args):
    found = False
    if (args.amount is None and
            args.description is None and
            args.type is None):
            print("Nothing to update.")
            return
    for expense in expenseslist:
        if args.id == expense["id"]:
            found = True
            if args.amount is not None:
                if args.amount < 0:
                    print("u can not add negative amount")
                    return
                expense["amount"] = args.amount
            if args.description is not None:
                if args.description == "":
                    print("u can not write nothing")
                    break
                expense["description"] = args.description
            if args.type is not None:
                expense["category"] = args.type
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            expense["date_u"] = time
            break
    if not found:    
        print("no expense with this id")
        return
    savetofile(expenseslist)
    printlist(expenseslist)
def budget_(args):
    if args.budget < 0:
        print("no negative budget")
        return
    with open("budget.json", "w") as file:
        json.dump(args.budget, file, indent=4)
    return args.budget
def help_e(args):
    command_list = [
        "add      - add a expense",
        "list     - show all expenses",
        "update   - edit an expense",
        "delete   - delete a expense by ID",
        "empty    - remove all expenses",
        "help     - show this help",
        "type - choose a category to list expenses with such category",
        "listm   - choose a month to check costs in said month",
        "summary  - to find out a total costs for all the expences", 
        "budget   - to set a budget, you can get a warning if you are over a budget and check a summary "]
    for command in command_list:
        print(command)
def fcategory_list(expenseslist, args):
    found = False
    for expense in expenseslist:
        if expense["category"] == args.type:
            found = True
            print(f'{expense["id"]}. {expense["description"]}, {expense["amount"]}, ({expense["category"]})')
    if not found:
        print("There are no expenses in this category.")   
def list_m(expenseslist, args):
    if args.month > 12 or args.month < 1:
        print("month can be from 1 to 12")
        return
    summary_m = 0
    for expense in expenseslist:
        date = datetime.strptime(expense["date"], "%Y-%m-%d %H:%M")
        if date.month == args.month:
            summary_m += expense["amount"]
    print("expenses for a month:", summary_m)
def empty(expenseslist, args):
    print("deleted")
    expenseslist.clear()
    savetofile(expenseslist)
def list_(expenseslist, budget, args):
    printlist(expenseslist)
    if budget is not None:
        print(f"Your budget: {budget}") 
def summary(expenseslist, budget, args):
    summary = 0
    for expense in expenseslist:
        summary += expense["amount"]
    print(f"Total expenses: {summary}")
    if budget is not None and summary > budget:
        print("Warning! You exceeded your budget.")
def export_expenses(expenseslist, args):
    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Description", "Amount", "Category", "Created", "Updated"])
        for expense in expenseslist:
            writer.writerow([
                expense["id"],
                expense["description"],
                expense["amount"],
                expense["category"],
                expense["date"],
                expense["date_u"]
            ])
    print("Expenses exported to expenses.csv")
    return
def main():
    try:
        with open("budget.json", "r") as file:
            budget = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        budget = None
    try:
        with open("expenses.json", "r") as file:
            expenseslist = json.load(file) 
    except FileNotFoundError:
        expenseslist = []
    except json.JSONDecodeError:
        expenseslist = []
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", type=int, required=True)
    update_parser.add_argument("--amount", type=float)
    update_parser.add_argument("--description")
    update_parser.add_argument("--type", choices=["needed", "not needed"])

    
    budget_parser = subparsers.add_parser("budget")
    budget_parser.add_argument("--budget", type=float, required=True)

    empty_parser = subparsers.add_parser("empty")
    list_parser = subparsers.add_parser("list")
    summary_parser = subparsers.add_parser("summary")
    export_parser = subparsers.add_parser("export")
    help_parser = subparsers.add_parser("help")
    type_parser = subparsers.add_parser("type")
    type_parser.add_argument("--type", choices=["needed", "not needed"], required=True)
    

    listm_parser = subparsers.add_parser("listm")
    listm_parser.add_argument("--month", type=int, required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--type", choices=["needed", "not needed"], required=True)
    args = parser.parse_args()
    if args.command == "delete" and len(expenseslist) == 0:
        print("nothing to delete so far")
        return
    if args.command is None:
        parser.print_help()
        return
    if args.command == "add":
        add_expense(expenseslist, args)
    elif args.command == "delete":
        delete_expense(expenseslist, args)
    elif args.command == "update":
        update_expense(expenseslist, args)
    elif args.command == "type":
        fcategory_list(expenseslist, args)
    elif args.command == "empty":
        empty(expenseslist, args)
    elif args.command == "help":
        help_e(args)
    elif args.command == "listm":
        list_m(expenseslist, args)
    elif args.command == "budget":
        new_budget = budget_(args)
        if new_budget is not None:
            budget = new_budget
    elif args.command == "summary":
        summary(expenseslist, budget, args)
    elif args.command == "list":
        list_(expenseslist, budget, args)
    elif args.command == "export":
        export_expenses(expenseslist, args)
main()