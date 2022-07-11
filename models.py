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
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.title = title
    daily_task_frequency: int


class Scheduled(DailyTask):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)
        self.title = title
    scheduled_days_between: int


class User:
    def __init__(self, name: str, password: str, **kwargs ):
        self.name = name
        self.password = password
        self.points = 0


t_1 = Scheduled("take a shit", task_compleated=True, scheduled_days_between=3, daily_task_frequency=14)
print(t_1.scheduled_days_between)

