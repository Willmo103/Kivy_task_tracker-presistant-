from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
# Builder.load_file("login.kv")


class MainWidget(GridLayout):
    header_msg = StringProperty("Test Test")
    username_input = StringProperty("Enter Your Username")
    password_input = StringProperty("Enter Your Password")
    submit_enabled = False
    login_credentials = {"username": "", "password": ""}


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

    def clear_username(self):
        self.username_input = ""

    def clear_password(self):
        self.password_input = ""

    def check_username(self):
        if not self.username_input:
            self.username_input = "Enter your username"

    def validate_password(self, widget):
        self.login_credentials.update({"password": widget.user_password.text})


class TaskApp(App):
    pass


TaskApp().run()

