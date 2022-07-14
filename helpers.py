import json
import os


def read_json() -> dict:
    with open("data/user_info.json", "r") as f:
        data: dict = json.load(f)
        return data


def write_json(data: dict):
    with open("data/user_info.json", "w") as f:
        json.dump(data, f)


def is_users():
    data: dict = read_json()
    users: list = data.get('users')
    if len(users) == 0:
        return False
    else:
        return True


def init_json(self):
    """
    This is the initialization process for the startup of a new
    installation of this application. it will setup the json database and
    structure to allow for multiple users on the same device. the structure will be:
    { users: [{
        "username": "username",
        "password": "password",
        "user_tasks": [
            {task1}, {task2}, {task3},
            ],
        "user_daily_tasks": [
            {task1}, {task2}, {task3},
            ],
        "user_tasks_completed": [
            {task1}, {task2}, {task3},
            ],
        "user_points": points,
        }, etc...]
    """
    try:
        read_json()
    except FileNotFoundError:
        if not os.path.exists("data"):
            os.mkdir("data")
        json_structure = {
            "users": []
        }
        write_json(json_structure)
    users = read_json()
    if len(users.get('users')) == 0:
        self.state_no_users = True
    else:
        self.state_no_users = False
        data = read_json()
        users = data.get("users")
        for user in users:
            name = user.get("username")
            password = user.get("password")
            self.stored_users.append({"username": name, "password": password})
        # print(self.stored_users)


