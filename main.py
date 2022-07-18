from abc import ABC

from kivy.config import Config

# Portrait display
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '854')

# landscape display
# Config.set('graphics', 'width', '854')
# Config.set('graphics', 'height', '480')

from kivy.utils import get_color_from_hex
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout

from kivymd.uix.screen import MDScreen

from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# Additional Imports
from models import User, Task
from helpers import read_json, write_json, is_users, init_json

# Global Variables
VALIDATED_USER = None


# TODO: Build out the display for the stack layout of the tasks.


class LoginScreen(Screen):
    # ===== local imports of helper functions, models ===== #
    from helpers import init_json

    # ===== validation string properties ===== #
    username_input = StringProperty("Enter Your Username")
    password_input = StringProperty("Enter Your Password")
    header_text = StringProperty("User Login")
    stored_users: list[User] = []

    # ===== States ===== #
    state_valid_user = False
    state_invalid_username = False
    state_invalid_password = False
    state_no_users = True

    # ==== props ===== #
    current_user: User = None

    # ===== init =====#
    def __init__(self, **kwargs):
        self.init_json()
        self.new_user_entry()
        super(Screen, self).__init__(**kwargs)

    def clear_username(self):
        self.username_input = ""

    def clear_password(self, widget):
        self.password_input = ""
        widget.password = True

    def new_user_entry(self):
        if self.state_no_users:
            self.username_input = "Enter your new username"
            self.password_input = "Enter your new password"
            self.header_text = "New User"

    def validate(self, password, username):
        self.state_invalid_password = False
        self.state_invalid_username = False
        if not self.state_no_users:
            if username == "" or username == "Enter Your Username":
                self.state_invalid_username = True
            elif password == "" or password == "Enter Your Password":
                self.state_invalid_password = True
                return
            for i in range(0, len(self.stored_users)):
                current_username = self.stored_users[i].get_username()
                current_password = self.stored_users[i].get_password()
                if str(current_password) == password and current_username.lower() == username.lower():
                    self.state_valid_user = True
                    self.current_user = self.stored_users[i]
                    return
                elif str(current_password) == password or current_username.lower() == username.lower():
                    if str(current_password) != password:
                        self.state_invalid_password = True
                    else:
                        self.state_invalid_password = False
                    if str(current_username).lower() != username.lower():
                        self.state_invalid_username = True
                    else:
                        self.state_invalid_username = False
        elif self.state_no_users and username != "" or username != "Enter Your Username" and \
                password != "" or password != "Enter Your Password":

            data = read_json()
            users = data.get("users")
            new_user = User(username, password)
            users.append(new_user.to_dict())
            data.update({"users": users})
            write_json(data)
            self.state_valid_user = True
            self.current_user = new_user


class ListViewScreen(Screen):
    state_user_tasks_generated = False
    current_user: User = None
    tasks: list[Task] = None
    completed: list[Task] = None
    selected_task = None

    task_label: str = StringProperty("")
    task_buttons: list[Button] = []

    # Layout Widgets
    top_layout = None
    header_label = None
    stack_layout = None
    second_grid = None
    add_task_button = None
    view_completed_tasks = None

    def __init__(self, **kwargs):
        super(ListViewScreen, self).__init__(**kwargs)
        self.init_layout()

    def init_layout(self):

        self.header_label = Label(
            # ids="header",
            pos_hint={"center_x": .5, "center_y": .9},
            size_hint=(1, .1),
            font_size=(dp(60)),
            text=self.task_label
        )

        self.stack_layout = StackLayout(
            pos_hint={"center_x": .5, "center_y": .8},
            size_hint=(1, .6),
            padding=(dp(4)),
            orientation="lr-tb",
            spacing=(dp(3), dp(3))
        )

        self.second_grid = GridLayout(
            # ids="button_field",
            cols=2,
            pos_hint={"center_x": .5, "center_y": .2},
            size_hint=(1, .15),
            padding=(dp(8))
        )

        self.add_task_button = Button(
            # ids="add_task",
            text="Add Task",
            size_hint=(.45, .45),
            pos_hint={"center_x": .25, "center_y": .2},
            background_normal="",
            background_color=get_color_from_hex("#296ead")
        )

        self.view_completed_tasks = Button(
            # ids="view_completed_tasks",
            text="Completed Tasks",
            size_hint=(.45, .45),
            pos_hint={"center_x": .75, "center_y": .2},
            background_normal="",
            background_color=get_color_from_hex("#931858")
        )

        self.top_layout = GridLayout(rows=3)

        self.add_widget(self.top_layout)
        self.top_layout.add_widget(self.header_label)
        self.top_layout.add_widget(self.stack_layout)
        self.second_grid.add_widget(self.add_task_button)
        self.second_grid.add_widget(self.view_completed_tasks)
        self.top_layout.add_widget(self.second_grid)

    def init_user_tasks(self):
        self.tasks = self.current_user.get_tasks()
        self.completed = self.current_user.get_completed_tasks()
        self.header_label.text = f"{self.current_user.get_username().title()}'s Tasks:"

        if self.tasks and not self.state_user_tasks_generated:
            for task in self.tasks:
                color = ""
                if task.get_urgency() == "low":
                    color = "7ACCF5"
                elif task.get_urgency() == "medium":
                    color = "#F5E77A"
                elif task.get_urgency() == "high":
                    color = "#F57a7c"
                button = TaskButton(
                    size_hint=(.2, .2),
                    text=task.get_title(),
                    background_normal="",
                    background_color=get_color_from_hex(f"{color}"),
                )
                self.task_buttons.append(button)
            for button in self.task_buttons:
                self.stack_layout.add_widget(button)
        else:
            self.task_label = "No tasks to display"
            print("No tasks to display")
        self.state_user_tasks_generated = True


    def open_task_window(self, text):
        selected_task: Task
        for task in self.tasks:
            if text == task.get_title():
                selected_task = task
                break
            else:
                continue
        self.selected_task = selected_task


class TaskButton(Button):
    ...


class AddTaskScreen(Screen):
    ...


class ViewTaskScreen(Screen):
    selected_task: Task = None
    task_text = StringProperty("")

    def generate_text(self):
        print(self.selected_task)
        # text = self.selected_task.to_dict()
        # self.task_text = text

    def update_selected_task(self, task: Task):
        self.selected_task = task

    def clear_selected_task(self):
        self.selected_task = None


class WindowManager(ScreenManager):
    current_user: User = None
    selected_task: Task = None

    def update_current_user(self, user: User):
        self.current_user = user

    def update_selected_task(self, task: Task):
        self.selected_task = task

    def pass_selected_task(self):
        return self.selected_task

    def clear_selected_task(self):
        self.selected_task = None

    ...


class TaskApp(App):
    def build(self):
        sm = WindowManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ListViewScreen(name="list_view"))
        sm.add_widget(ViewTaskScreen(name="view_task"))
        sm.add_widget(AddTaskScreen(name="add_task"))
        return sm


if __name__ == '__main__':
    TaskApp().run()
