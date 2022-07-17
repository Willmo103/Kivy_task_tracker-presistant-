from datetime import datetime


class Task:
    def __init__(self, title: str,
                 description: str = "",
                 urgency: int = None,
                 is_due: bool = False,
                 due_date: datetime = None,
                 point_value: int = 0,
                 completed=False, **kwargs):
        self.title = title
        self.description = description
        self.urgency = urgency
        self.is_due = is_due
        if self.is_due:
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

    def set_completed(self, completed):
        self.completed = completed

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

class DailyTask(Task):
    daily_task_frequency: int

    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.title = title


class Scheduled(DailyTask):
    scheduled_days_between: int

    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.title = title


class User:
    tasks = []
    points = 0
    completed_tasks = []

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password

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
        data = {
            "name": self.name,
            "password": self.password,
            "points": self.points,
            "tasks": self.tasks,
            "completed": self.completed_tasks
        }
        return data


def user_from_dict(data: dict) -> User:
    """
    This function is called to generate a User object
    from the JSON file during the initialization
    of the program.
    :param: dict version of a User Class Object
    """
    user = User(
        data.get('name'),
        data.get('password')
    )
    user.set_points(data.get("points"))
    user.set_tasks(data.get("tasks"))
    user.set_completed_tasks(data.get("completed"))
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

    :param dict version of a Task Class Object"""

    task = Task(
        data.get("title"),
        data.get("description"),
        data.get("urgency"),
        data.get("is_due"),
        data.get("due_data"),
        data.get("points"),
        data.get("completed")
    )
    return task
