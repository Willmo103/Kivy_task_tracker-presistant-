from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# Additional Imports
from models import User

# Global Variables
VALIDATED_USER = None


# TODO: Display invalid password / invalid username if login fails
# TODO: Disable the submit button if both username and password aren't filled in
# TODO: Build out the display for the stack layout of the tasks.


class LoginScreen(Screen):
    # ===== local imports of helper functions, models ===== #
    from helpers import read_json, write_json, is_users, init_json


    # ===== validation string properties ===== #
    username_input = StringProperty("Enter Your Username")
    password_input = StringProperty("Enter Your Password")
    header_text = StringProperty("U S E R   L O G I N")
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
            self.header_text = "N E W   U S E R"

    def validate(self, password, username):
        if not self.state_no_users:
            for i in range(0, len(self.stored_users)):
                current_username = self.stored_users[i].get_username()
                current_password = self.stored_users[i].get_password()
                if str(current_password) == password and current_username.lower() == username.lower():
                    self.state_valid_user = True
                    self.current_user = self.stored_users[i]
                elif str(current_password) == password or current_username.lower() == username.lower():
                    if str(current_password) != password:
                        self.state_invalid_password = True
                    else:
                        self.state_invalid_password = False
                    if str(current_username).lower() != username.lower():
                        self.state_invalid_username = True
                    else:
                        self.state_invalid_username = False
        elif self.state_no_users and username != '' and password != "":
            data = self.read_json()
            users = data.get("users")
            users.append(User(username, password))
            self.state_valid_user = True


class ListViewScreen(Screen):
    current_user = None

    def test(self):
        print(self.current_user.to_dict())
    ...


class AddTaskScreen(Screen):
    ...


class WindowManager(ScreenManager):
    current_user: User = None
    def update_current_user(self, user: User):
        self.current_user = user
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
