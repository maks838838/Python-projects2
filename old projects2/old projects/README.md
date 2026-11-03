# Task Tracker CLI - https://github.com/maks838838/Python-projects2/blob/main/task.py
https://roadmap.sh/projects/task-tracker

A simple command-line task manager written in Python.

This project stores tasks in a local `tasks.json` file and allows you to create, edit, delete, and organize tasks by their status.

## Features

- Add new tasks
- Delete tasks by ID
- Edit task descriptions
- Update task status
- List all tasks
- List tasks by status
- Automatically create `tasks.json` if it does not exist
- Store data in JSON format
- Track:
  - Task ID
  - Description
  - Status
  - Creation date
  - Last update date
- Automatically renumber task IDs after deleting tasks
- Handles invalid IDs and missing JSON files gracefully

---

## Requirements

- Python 3.x

No external libraries are required.

---

## Files

```
task.py
tasks.json
```

`tasks.json` is automatically created after adding the first task.

---

## Running the program

```bash
python task.py
```

---

## Available Commands

| Command | Description |
|----------|-------------|
| `add` | Add a new task |
| `list` | Show all tasks |
| `change` | Change a task description |
| `delete` | Delete a task by ID |
| `update` | Change task status |
| `status list` | Show tasks with a selected status |
| `empty` | Remove all tasks |
| `help` | Show available commands |
| `end` | Exit the program |

---

## Task Statuses

Tasks can have one of the following statuses:

- `to do`
- `in progress`
- `done`

---

## Example

```
Print a command: add

write what u want to add:
Finish Python project

tasks:
1. Finish Python project (to do)
```

Updating a task:

```
Print a command: update

write a id of a task u want to update:
1

write new status:
done
```

Listing tasks:

```
Print a command: list

tasks:
1. Finish Python project (done)
```

---

## Data Format

Tasks are stored inside `tasks.json` as dictionaries.

Example:

```json
[
    {
        "id": 1,
        "description": "Finish Python project",
        "status": "done",
        "date": "2026-07-19 16:42",
        "date_u": "2026-07-19 17:18"
    }
]
```

---

## Error Handling

The program handles:

- Missing `tasks.json`
- Empty JSON files
- Invalid task IDs
- Invalid task statuses
- Empty task descriptions
- Unknown commands

---

## Future Improvements

Possible future features include:

- Search tasks
- Sort tasks
- Priority levels
- Due dates
- Task history
- Command-line arguments instead of interactive input
- Colored terminal output

## Author

Created by Maks838838 as a Python learning project.
