#!/bin/python
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.garden.knob import  Knob
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.progressbar import ProgressBar
from kivy.config import Config
from config_manager import ConfigManager
from screens.Activity import Activity
from screens.Cooking import Cooking
from screens.MainMenu import MainMenu
from screens.NewBrewBlurring import NewBrewBlurring
from screens.SavedConfigs import SavedConfigs
from screens.SaveConfig import SaveConfig

Builder.load_file('layouts/main.kv')

class ScreenManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(ScreenManager, self).__init__(*args, **kwargs)
        self.screens = [
                SavedConfigs(name='SavedConfigs'),
                NewBrewBlurring(name='NewBrewBlurring'),
                Cooking(name='Cooking'),
                MainMenu(name='MainMenu'),
                SaveConfig(name='SaveConfig'),
            ]
        [self.add_widget(self.screens[i]) for i in range(len(self.screens))]
        self.stack = [self.screens[0].name]

    def back(self, data={}):
        self.stack = self.stack[:-1]
        self.get_screen_by_name(self.stack[-1]).on_resume(data)
        self.current = self.stack[-1]

    def go(self, name, data={}):
        self.get_screen_by_name(name).on_start(data)
        if name == 'MainMenu':
            self.stack = [name]
        else:
            self.stack.append(name)
        self.current = name

    def get_screen_by_name(self, name):
        return next((s for s in self.screens if s.name == name), None)


class MainApp(App):
    sm = ScreenManager(transition=FadeTransition());
    def build(self):
        return self.sm


if __name__ == "__main__":
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')
    MainApp().run()
