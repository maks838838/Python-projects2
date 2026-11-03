import json
import csv
from datetime import datetime

def id_check(expenseslist):
    expected_id = 1
    for expense in expenseslist:    
        if expense["id"] != expected_id:
            expense["id"] = expected_id
        expected_id += 1
def savetofile(expenseslist):
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
def add_expense(expenseslist, category_list):
    description = input("write the description of an expense: ").strip()
    if description == "":
        print("u can not add nothing")
        return
    try:
        amount = float(input("write the amount: ").strip())
    except ValueError:
        print("it has to be a number")
        return
    if amount < 0:
        print("u can not add negative amount")
        return    
    category = input("write a category: needed, not needed: ").strip()
    if category not in category_list:
        print("wrong category")
        return
    if len(expenseslist) == 0:
            expense_id = 1
    else:
        expense_id = expenseslist[-1]["id"]+1
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_expense = {"id": expense_id, "amount": amount, "description": description, "category": category, "date": time, "date_u":"No changes"}
    expenseslist.append(new_expense)
    printlist(expenseslist)
    savetofile(expenseslist)
def delete_expense(expenseslist):         
    try:  
        dexpense_id = int(input("write a id of a expense u want to delete: "))
    except ValueError:
        print("no such id is possible")
        return
    found = False
    for expense in expenseslist:
        if dexpense_id == expense["id"]:
            found = True
            expenseslist.remove(expense)
            break
    if not found:    
        print("no expense with this id")
        return
    printlist(expenseslist)
    print(dexpense_id, "expense was deleted")
    savetofile(expenseslist)
def update_expence(expenseslist):
    try:
        dexpense_id = int(input("write a id of a expense u want to update: "))
    except ValueError:
        print("no such id")
        return
    found = False
    for expense in expenseslist:
        if dexpense_id == expense["id"]:
            found = True
            what = input("what u want to change amount or description: ")
            if what == "amount":
                try: 
                    amount = float(input("write new amount: ").strip())
                except ValueError:
                    print("incorrect input")
                    return
                if amount < 0:
                    print("u can not add negative amount")
                    return
                expense["amount"] = amount
            elif what == "description":
                new_description = input("write new description: ").strip()
                if new_description == "":
                    print("u can not write nothing")
                    break
                expense["description"] = new_description
            else:
                print("incorrect input")
                return
            time = datetime.now().strftime("%Y-%m-%d %H:%M")
            expense["date_u"] = time
            break
    if not found:    
        print("no expense with this id")
        return
    printlist(expenseslist)
    savetofile(expenseslist)
def budget_():
    try:
        budget = float(input("write a budget for a month: "))
        if budget < 0:
            print("no negative budget")
            return
    except ValueError:
        print("it needs to be a number")
        return
    with open("budget.json", "w") as file:
        json.dump(budget, file, indent=4)
    return budget
def help_e():
    command_list = [
        "add      - add a expense",
        "list     - show all expenses",
        "update   - edit an expense",
        "delete   - delete a expense by ID",
        "empty    - remove all expenses",
        "end      - exit the program",
        "help     - show this help",
        "category list - choose a category to list expenses with such category",
        "list m   - choose a month to check costs in said month",
        "summary  - to find out a total costs for all the expences", 
        "budget   - to set a budget, you can get a warning if you are over a budget and check a summary "]
    for command in command_list:
        print(command)
def fcategory_list(expenseslist, category_list):
    expense_category = input("write category u want a list of: ").strip()
    if expense_category not in category_list:
        print("invalid category")
        return
    found = False
    for expense in expenseslist:
        if expense["category"] == expense_category:
            found = True
            print(f'{expense["id"]}. {expense["description"]}, {expense["amount"]}, ({expense["category"]})')
    if not found:
        print("There are no expenses in this category.")   
def list_m(expenseslist):
    try:
        month = int(input("costs on which month? "))
    except ValueError:
        print("you need to write a number of the month")
        return
    if month > 12 or month < 1:
        print("month can be from 1 to 12")
        return
    summary_m = 0
    for expense in expenseslist:
        date = datetime.strptime(expense["date"], "%Y-%m-%d %H:%M")
        if date.month == month:
            summary_m += expense["amount"]
    print(summary_m)
def empty(expenseslist):
    are_u_sure = input("are u sure y/n? ").strip().lower()
    if are_u_sure == "y":
        print("deleted")
        expenseslist.clear()
        savetofile(expenseslist)
        return
def list_(expenseslist, budget):
    printlist(expenseslist)
    if budget is not None:
        print(f"Your budget: {budget}") 
def summary(expenseslist, budget):
    summary = 0
    for expense in expenseslist:
        summary += expense["amount"]
    print(summary)
    if budget is not None and summary > budget:
        print("Warning! You exceeded your budget.")
def export_expenses(expenseslist):
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
    category_list = ["needed", "not needed"]
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
    while True:
        command = input("Print a command: ").strip().lower()
        if command == "delete" and len(expenseslist) == 0:
            print("nothing to delete so far")
            continue
        if command == "add":
            add_expense(expenseslist, category_list)
        elif command == "delete":
            delete_expense(expenseslist)
        elif command == "update":
            update_expence(expenseslist)
        elif command == "category list":
            fcategory_list(expenseslist, category_list)
        elif command == "empty":
            empty(expenseslist)
        elif command == "help":
            help_e()
        elif command == "list m":
            list_m(expenseslist)
        elif command == "budget":
            new_budget = budget_()
            if new_budget is not None:
                budget = new_budget
        elif command == "summary":
            summary(expenseslist, budget)
        elif command == "list":
            list_(expenseslist, budget)
        elif command == "":
            continue
        elif command == "end":
            break
        elif command == "export":
            export_expenses(expenseslist)
        else:
            print("incorrect command")
            continue
main()
