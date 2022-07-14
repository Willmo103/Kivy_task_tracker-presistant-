from datetime import datetime


class Task:
    task_title: str
    task_description: str = ""
    task_urgency: int = None
    task_is_due: bool = False
    task_due_date: datetime
    task_point_value: int
    task_completed = False
    def __init__(self, title: str, **kwargs):
        self.title = title
        # urgency should be in a scale of 1 being lowest of point
        # 2, and 3 scaling up.

        # need to figured out time and shit



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
    def __init__(self, name: str, password: str, **kwargs ):
        self.name = name
        self.password = password
        self.points = 0


