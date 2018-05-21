from kivy.uix.screenmanager import ScreenManager
from screens.Activity import Activity
from screens.NewBrewBlurring import NewBrewBlurring
from screens.ScreenManager import ScreenManager

from kivy.lang import Builder

Builder.load_file('layouts/main.kv')

class ScreenManagement(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(ScreenManagement, self).__init__(*args, **kwargs)
        self.screens = [
                SavedConfigs(name='SavedConfigs'),
                NewBrewBlurring(name='NewBrewBlurring'),
                Cooking(name='Cooking'),
                MainMenu(name='MainMenu'),
            ]
        [self.add_widget(self.screens[i]) for i in range(len(self.screens))]
        self.stack = [self.screens[0].name]

    def back(self):
        name = self.stack[-1]
        self.stack = self.stack[:-1]
        self.get_screen_by_name(self.stack[-1]).on_resume(name)
        self.current = self.stack[-1]

    def go(self, name):
        self.get_screen_by_name(name).on_start(self.stack[-1])
        self.current = name
        if name == 'MainMenu':
            self.stack = [name]
        else:
            self.stack.append(name)

    def get_screen_by_name(self, name):
        return next((s for s in self.screens if s.name == name), None)

