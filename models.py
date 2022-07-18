import json
import os
from datetime import datetime




class Task:
    def __init__(self, title: str,
                 description: str = "",
                 urgency: str = "low",
                 is_due: bool = False,
                 due_date: any = None,
                 point_value: int = 0,
                 completed=False, **kwargs):
        self.title = title
        self.description = description
        self.urgency = urgency
        self.is_due = is_due
        self.due_date = due_date
        self.point_value = point_value
        self.completed = completed

    def get_title(self):
        return self.title

    def set_title(self, title: str):
        self.title = title

    def get_description(self):
        return self.description

    def set_description(self, description: str):
        self.description = description

    def get_urgency(self):
        return self.urgency

    def set_urgency(self, urgency: int):
        self.urgency = urgency

    def get_is_due(self):
        return self.is_due

    def set_is_due(self, is_due):
        self.is_due = is_due

    def get_due_date(self):
        return self.due_date

    def set_due_date(self, due_date: datetime):
        self.due_date = due_date

    def get_point_value(self):
        return self.point_value

    def set_point_value(self, point_value: int):
        self.point_value = point_value

    def get_completed(self):
        return self.completed

    def set_completed(self):
        self.completed = True

    def to_dict(self) -> dict:
        task = {
            "title": self.title,
            "description": self.description,
            "urgency": self.urgency,
            "is_due": self.is_due,
            "due_date": self.due_date,
            "point_value": self.point_value,
            "completed": self.completed
        }
        return task


class User:

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password
        self.tasks: list[Task] = []
        self.points = 0
        self.completed_tasks: list[Task] = []

    def set_username(self, username: str):
        self.name = username

    def get_username(self):
        return self.name

    def set_password(self, password: str):
        self.password = password

    def get_password(self):
        return self.password

    def set_tasks(self, tasks: list[Task]):
        self.tasks = tasks

    def get_tasks(self):
        return self.tasks

    def set_points(self, points: int):
        self.points = points

    def get_points(self):
        return self.points

    def set_completed_tasks(self, completed_tasks: list[Task]):
        self.completed_tasks = completed_tasks

    def get_completed_tasks(self):
        return self.completed_tasks

    def add_task(self, task: Task, tasks: list = None):
        if tasks:
            for task in tasks:
                self.tasks.append(task)
        else:
            self.tasks.append(task)

    def complete_task(self, task: Task):
        self.completed_tasks.append(self.tasks.pop(self.tasks.index(task)))

    def to_dict(self) -> dict:
        tasks = []
        completed = []
        for task in self.tasks:
            tasks.append(task.to_dict())
        for completed_task in self.completed_tasks:
            completed.append(completed_task.to_dict())
        data = {
            "name": self.name,
            "password": self.password,
            "points": self.points,
            "tasks": tasks,
            "completed": completed
        }
        return data

    def save(self):
        previous_version: dict
        current_version = self.to_dict()
        json_data = read_json()
        users: list[dict] = json_data.get("users")
        for user in users:
            if user.get("name") == self.name and user.get("password") == self.password:
                previous_version_index = users.index(user)
                break
        users.pop(previous_version_index)
        users.append(current_version)
        json_data['users'] = users
        write_json(json_data)


def user_from_dict(data: dict) -> User:
    """
    This function is called to generate a User object
    from the JSON file during the initialization
    of the program.
    :param: dict version of a User Class Object
    """
    tasks: list[Task] = []
    completed: list[Task] = []

    # call __init__ method on User
    user: User = User(
        data.get('name'),
        data.get('password')
    )

    # Use Setter to set the points
    user.set_points(data.get("points"))

    # loop though and init tasks from saved tasks
    dict_tasks: list[dict] = data.get("tasks")
    for task in dict_tasks:
        tasks.append(task_from_dict(task))
    user.set_tasks(tasks)

    # loop though and init tasks from saved completed tasks
    dict_completed: list[dict] = data.get("completed")
    for task in dict_completed:
        completed.append(task_from_dict(task))
    user.set_completed_tasks(completed)
    return user


def task_from_dict(data: dict) -> Task:
    """ will take the version of the class saved by the Task class
    method to_dict:

            "title": self.title,
            "description": self.description,
            "urgency": self.urgency,
            "is_due": self.is_due,
            "due_date": self.due_date,
            "point_value": self.point_value,
            "completed": self.completed

    and initiate a new Task class object from the dict
    :param: data a dict version of a Task Class Object"""

    task: Task = Task(
        data.get("title"),
        data.get("description"),
        data.get("urgency"),
        data.get("is_due"),
        data.get("due_date"),
        data.get("points"),
        data.get("completed")
    )
    return task


class TaskData:
    selected_task = None

    def update_selected_task(self, task: Task):
        self.selected_task = task

    def pass_selected_task(self):
        return self.selected_task

    def clear_selected_task(self):
        self.selected_task = None


class UserData:
    current_user: User = None

    def update_current_user(self, user: User):
        self.current_user = user

    def pass_current_user(self) -> User:
        return self.current_user

    def clear_current_user(self):
        self.current_user = None


# from models import user_from_dict


def read_json() -> dict:
    with open("data/user_info.json", "r") as f:
        data: dict = json.load(f)
        return data


def write_json(data: dict):
    with open("data/user_info.json", "w") as f:
        json.dump(data, f)


def is_users() -> bool:
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
            user = user_from_dict(user)
            self.stored_users.append(user)
            # print(user.to_dict())
        # print(self.stored_users)


