from kivy.uix.screenmanager import Screen
from screens.Activity import Activity

class MainMenu(Screen, Activity):

    def new_brew(self):
        self.manager.go('NewBrewBlurring')

    def saved_configs(self):
        self.manager.go('SavedConfigs')
