from kivy.uix.screenmanager import Screen
from screens.Activity import Activity

class Cooking(Screen, Activity):
    def menu(self):
        self.manager.go('MainMenu')
