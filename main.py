from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout


class MainWidget(GridLayout):
    header_msg = StringProperty("Test Test")


class TaskApp(App):
    pass


TaskApp().run()

