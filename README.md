<h1>Task Tracker CLI App</h1>
This application is a todolist app with a command line interface. The project is built off of typer and rich. In order to run any command, the following must precede the name and parameters of the command:
```python
python task-cli.py [name of command]
```
<h2>Initialization</h2>
All tasks are stored in a JSON file which is not yet created when ```task-cli.py``` is downlaoded. In order to initialize this file, use the following command:
```python
python task-cli.py init
```
<h2>Commands</h2>
Below is a list of all commands that can be done. Remember that ```python task-cli.py``` must precede the name of all commands.
```
add
delete
update
mark
id
ls
clear
init
```
Some of these commands can be ran without extra parameters(ls, clear, etc). Others must have parameters specified with the ```--[parameter name]``` syntax. You can append ```--help``` to the end of a command to see a list of its parameters.
