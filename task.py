import json
## FUNCRION TO LIST TASKS
def id_check(tasklist):
    expected_id = 1
    for task in tasklist:    
        if task["id"] != expected_id:
            task["id"] = expected_id
        expected_id += 1
def savetofile(tasklist):
    with open("tasks.json", "w") as file:
        json.dump(tasklist, file)

def printlist(tasklist):
    print("tasks:")
    if len(tasklist) == 0: 
        print("you have nothing to do")
    id_check(tasklist)
    for task in tasklist:
        print(f'{task["id"]}. {task["description"]}, ({task["status"]})')
    
def usetask():
    status_list = ["to do", "in progress", "done"]
## try opening file to read and load a list and not break the code
    try:
        with open("tasks.json", "r") as file:
            tasklist = json.load(file) 
    except FileNotFoundError:
        tasklist = []
    except json.JSONDecodeError:
        tasklist = []
    while True:
## TAKING A COMMAND        
        input1 = input("Print a command: ").strip().lower()
        if input1 == "delete" and len(tasklist) == 0:
            print("nothing to delete so far")
            continue
## FUNCTION ADD
        if input1 == "add":
            add = input("write what u want to add: ").strip()
            if add == "":
                print("u can not add nothing")
                continue
            if len(tasklist) == 0:
                task_id = 1
            else:
                task_id = tasklist[-1]["id"]+1
            new_task = {"id": task_id, "description": add, "status": "to do"}
            tasklist.append(new_task)
            printlist(tasklist)
            savetofile(tasklist)
##FUNCTION DELETE
        elif input1 == "delete":
            try:  
                dtask_id = int(input("write a id of a task u want to delete: "))
            except ValueError:
                print("no such id")
                continue
            found = False
            for task in tasklist:
                if dtask_id == task["id"]:
                    found = True
                    tasklist.remove(task)
                    break
            if not found:    
                print("no task with this id")
                continue
            printlist(tasklist)
            print(dtask_id, "task was deleted")
            savetofile(tasklist)
##FUNCTION CHANGE
        elif input1 == "change":
            try:
                dtask_id = int(input("write a id of a task u want to delete: "))
            except ValueError:
                print("no such id")
                continue
            found = False
            for task in tasklist:
                if dtask_id == task["id"]:
                    found = True
                    add = input("wtite what u want to change into: ").strip()
                    task["description"] = add
                    break
            if not found:    
                print("no task with this id")
                continue
            printlist(tasklist)
            savetofile(tasklist)
##function update
        elif input1 == "update":
            try:
                dtask_id = int(input("write a id of a task u want to update: "))
            except ValueError:
                print("no such id")
                continue
            found = False
            for task in tasklist:
                if dtask_id == task["id"]:
                    found = True
                    add = input("write new status: ").strip()
                    if add not in status_list:
                        print("invalid status")
                        break
                    task["status"] = add
                    break
            if not found:    
                print("no task with this id")
                continue
            printlist(tasklist)
            savetofile(tasklist)
##functions status lists
        elif input1 == "status list":
            task_status = input("write status u want a list of: ").strip()
            if task_status not in status_list:
                print("invalid status")
                continue
            for task in tasklist:
                if task["status"] == task_status:
                    print(f'{task["id"]}. {task["description"]}, ({task["status"]})')

##empty help and incorrect comand, end,list
        elif input1 == "empty":
            tasklist = []
            savetofile(tasklist)
        elif input1 == "help":
            command_list = [
                "add      - add a task",
                "list     - show all tasks",
                "change   - edit a task",
                "delete   - delete a task by ID",
                "empty    - remove all tasks",
                "end      - exit the program",
                "help     - show this help",
                "update   - updates a status(to do, in progress, done)",
                "status list - choose a status to list taks with such status"]
            for command in command_list:
                print(command)
        elif input1 == "end":
            break
        elif input1 == "list":
            printlist(tasklist)
        else:
            print("incorrect command")
            continue
usetask()

