from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# TODO: figure out how to pass data between screens login -> list
# TODO: Display invalid password / invalid username if login fails
# TODO: Disable the submit button if both username and password aren't filled in
# TODO: Build out the display for the stack layout of the tasks.


class LoginScreen(Screen):
    # ===== local imports of helper functions, models ===== #
    from helpers import read_json, write_json, is_users, init_json
    from models import Task, User

    # ===== validation string properties ===== #
    username_input = StringProperty("Enter Your Username")
    password_input = StringProperty("Enter Your Password")
    stored_users: list = [dict, {str: any}]

    # ===== States ===== #
    state_valid_user = False
    state_invalid_user = False
    state_no_users = True

    # ==== props ===== #
    current_user: dict = None

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

    def validate(self, password, username):
        if not self.state_no_users:
            for i in range(2, len(self.stored_users)):
                current_username = self.stored_users[i].get("username").lower()
                current_password = self.stored_users[i].get("password")
                if str(current_password) == password and current_username == username.lower():
                    self.state_valid_user = True
                    self.current_user = self.stored_users[i]
                    print(self.state_valid_user)
                else:
                    self.state_invalid_user = True
        else:
            data = self.read_json()
            users = data.get("users")


class ListViewScreen(Screen):
    current_user = None

    def test(self):
        print(self.current_user)
    ...


class AddTaskScreen(Screen):
    ...


class WindowManager(ScreenManager):
    ...


class TaskApp(App):
    def build(self):
        sm = WindowManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ListViewScreen(name="list_view"))
        sm.add_widget(AddTaskScreen(name="add_task"))
        return sm


if __name__ == '__main__':
    TaskApp().run()
