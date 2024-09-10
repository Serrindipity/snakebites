path_to_todo_file = "filepath"
tasks = []
with open(path_to_todo_file, "r") as td:
    for line in td:
        if line.startswith("- ["):
            tasks.append(line)