from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen

sm = ScreenManager()

# Builder.load_file("login.kv")


class MainWidget(GridLayout):
    from helpers import read_json, write_json, is_users, init_json

    login_widget = ObjectProperty()

    username_input = StringProperty("Enter Your Username")
    password_input = StringProperty("Enter Your Password")
    stored_users: list = [dict, {str: any}]
    state_no_users = True
    submit_enabled = False
    header_msg = StringProperty("Test Test")
    state_valid_user = False

    def __init__(self, **kwargs):
        self.init_json()
        self.new_user_entry()
        super(MainWidget, self).__init__(**kwargs)

    def clear_username(self):
        self.username_input = ""

    def clear_password(self):
        self.password_input = ""

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
                    print(self.state_valid_user)


class TaskApp(App):
    pass


TaskApp().run()
