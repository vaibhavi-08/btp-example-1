import json
import os


def save_employees(file_path, employees):
    data = [emp.to_dict() for emp in employees]

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_employees(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r") as f:
        return json.load(f)