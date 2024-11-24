"""
The application should run from the command line, accept user actions and inputs as arguments, and store the tasks in a JSON file. The user should be able to:

Add, Update, and Delete tasks
Mark a task as in progress or done
List all tasks
List all tasks that are done
List all tasks that are not done
List all tasks that are in progress

Each task should have the following properties:

id: A unique identifier for the task
description: A short description of the task
status: The status of the task (todo, in-progress, done)
createdAt: The date and time when the task was created
updatedAt: The date and time when the task was last updated

The JSON file will be formatted as shown below:

{
    "0": { <--- the key is the ID
        "description": "blahblahblah",
        "status": "todo",
        "createdAt": someDate,
        "updatedAt": anotherDate
    },
    "1": { <--- the key is the ID
        "description": "blahblahblah",
        "status": "in-progress",
        "createdAt": someDate,
        "updatedAt": anotherDate
    }
}
"""

import json
import os
import typer
from typing_extensions import Annotated
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
from math import log10, ceil
from datetime import datetime

app = typer.Typer()
console = Console()

p_values = [
    Style(color="red", bold=True),
    Style(color="orange1", bold=True),
    Style(color="yellow", bold=True),
    Style(color="green", bold=True),
    Style(color="blue", bold=True),
    Style(color="purple", bold=True),
    Style(color="white", bold=True), 
]

status_styles = {
    "done": Style(color="green", bold=True),
    "in-progress": Style(color="cyan", bold=True),
    "todo": Style(color="white", bold=False),
}

path_to_json = f"{os.path.dirname(os.path.realpath(__file__))}/tasks.json"

def initialize():
    if not os.path.isfile(path_to_json):
        with open(path_to_json, "r") as tasks:
            json.dump({}, tasks, indent=4)
    
def get_priority_style(p: int) -> Style:
    if p < 7:
        return p_values[p-1]
    else:
        return p_values[6]

def get_status(done: bool, inprog: bool, todo: bool) -> str:
    if done:
        return "done"
    if inprog:
        return "in-progress"
    if todo:
        return "todo"
    return "N/A"

def make_task_obj(name: str = "", priority: int = 1, description: str = "", status: str = "todo") -> dict[str, str]:
    obj = {}
    obj["name"] = name
    obj["priority"] = priority
    obj["description"] = description
    obj["status"] = status
    obj["createdAt"] = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "12hour": datetime.now().strftime("%I:%M:%S %p")
    }
    obj["updatedAt"] = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "12hour": datetime.now().strftime("%I:%M:%S %p")
    }
    return obj

@app.command()
def add(task: str, desc: str = "", in_progress: bool = False, priority: int = 1):
    if priority > 0:
        with open(path_to_json, "r") as tasks:
            data = json.load(tasks)
            id = int(max(data.keys(), default=-1)) + 1
            task_obj = make_task_obj(task, priority, desc, "todo" if not in_progress else "in progress")
            data[str(id)] = task_obj

            with open(path_to_json, "w") as f:
                json.dump(data, f, indent=4)

        text = Text(f"Added {task} to list with Priority {priority}!")
        text.stylize("bold green", 6, len(task) + 6)
        text.stylize("bold blue", -ceil(log10(priority+1)) - 10)
        text.append(f" ID: {id}")
        console.print(Panel(text))
    else:
        panel = Panel(Text("Invalid priority value."), title="Error", border_style="red", title_align="left")
        console.print(panel)

@app.command()
def delete(task_id: int):
    task_id = str(task_id)
    text = Text("", style="bold red")

    with open(path_to_json) as f:
        data = json.load(f)
        if data.get((task_id)) is None:
            text.append(f"Unable to find task with ID {task_id}.")
        else:
            text.append(f"Succesfully deleted \"{data[task_id]['name']}\"\nID: {task_id}")
            data.pop(task_id)
            with open(path_to_json, "w") as g:
                json.dump(data, g, indent=4)
    
    console.print(Panel(text, border_style="red"))

@app.command()
def update(
    task_id: int,
    name: str = "",
    desc: str = "",     
):
    task_id = str(task_id)
    with open(path_to_json) as f:
        data = json.load(f)
        if data.get(task_id, None) is not None:
            data[task_id]["name"] = name if name != "" else data[task_id]["name"]
            data[task_id]["description"] = desc if desc != "" else data[task_id]["description"]
            with open(path_to_json, "w") as g:
                json.dump(data, g, indent=4)
            console.print(Panel(Text(f"Successfully updated task {task_id}!", style="bold green"), border_style="green"))
        else:
            console.print(Panel(Text("Invalid ID", style="bold red"), border_style="red"))

@app.command()
def mark(
    task_id: int,
    done: Annotated[bool, typer.Option(help="Mark as done")] = False,
    in_progress: Annotated[bool, typer.Option(help="Mark as in progress")] = False,
    todo: Annotated[bool, typer.Option(help="Mark as todo")] = False
):
    task_id = str(task_id)
    with open(path_to_json) as f:
        data = json.load(f)
        if data.get(task_id, None) is not None:
            new_status = get_status(done, in_progress, todo)
            data[task_id]["status"] = new_status

            update_value = data[task_id]["updatedAt"]
            update_value["date"] = datetime.now().strftime("%Y-%m-%d")
            update_value["time"] = datetime.now().strftime("%H:%M:%S")
            update_value["12hour"] = datetime.now().strftime("%I:%M:%S %p")

            with open(path_to_json, "w") as g:
                json.dump(data, g, indent=4)

            console.print(Panel(Text(f"Successfully marked as \"{new_status}\"", style="green bold"), border_style="green"))
        else:
            console.print(Panel(Text("Invalid ID", style="red bold"), border_style="red"))

@app.command()
def id(name: str):
    text = Text(f"Task name: {name}")
    text.stylize("bold yellow", -len(name) - 1)
    text.append("\nID: ")

    with open(path_to_json) as f:
        data = json.load(f)
        found_id_flag = False
        for k, v in data.items():
            if v["name"] == name:
                text.append(k)
                found_id_flag = True
        if not found_id_flag:
            text.append("N/A")

    console.print(Panel(text))

@app.command()
def ls(
    done: Annotated[bool, typer.Option(help="Only print completed tasks")] = False,
    in_progress: Annotated[bool, typer.Option(help="Only print in progress tasks")] = False,
    todo: Annotated[bool, typer.Option(help="Only print todo tasks")] = False
):
    with open(path_to_json) as f:
        num_of_tasks = len(json.load(f).keys())

    text = Text(f"Today's date: {datetime.now().strftime('%A, %B %d, %Y')}\n")
    text.stylize("yellow", 14)
    text.append(f"Number of tasks: {num_of_tasks}").stylize("cyan bold", -1)

    with open(path_to_json) as f:
        data = json.load(f)
        tasks_empty = True # a flag that is True when nothing was printed from the below code
        for k, v in data.items():
            tasks_empty = False

            if not (done and in_progress and todo):
                match v["status"]:
                    case "done":
                        if in_progress or todo:
                            continue

                    case "in-progress":
                        if done or todo:
                            continue
                    
                    case "todo":
                        if in_progress or done:
                            continue

                    case _:
                        pass

            t_style = get_priority_style(v["priority"])
            t_status_style = status_styles[v["status"]]

            t_text = Text(f"\n\n{v['name']}\n")
            t_text.stylize(t_style, 0, len(v["name"]) + 2)

            t_text.append(Text(f"Description | {v['description']}\n", style="white"))
            t_text.append(Text(f"Priority    | {v['priority']}\n", style="white")).stylize(t_style, -(ceil(log10(v["priority"] + 1)) + 1))
            t_text.append(Text(f"Status      | {v['status']}\n", style="white")).stylize(t_status_style, -len(v["status"]) - 1)
            t_text.append(Text(f"Created at  | {v['createdAt']['12hour']}\n", style="white")).stylize("yellow", -len(v['createdAt']['12hour']) - 1)
            t_text.append(Text(f"Updated at  | {v['updatedAt']['12hour']}\n", style="white")).stylize("yellow", -len(v['updatedAt']['12hour']) - 1)
            t_text.append(Text(f"ID          | {k}\n", style="white"))

            text.append(t_text)
        
        if tasks_empty: text.append("\nYou have no tasks.")

    console.print(Panel(text, title="Current tasks", title_align="left"))

@app.command()
def clear():
    console.clear()

if __name__ == "__main__":
    app()