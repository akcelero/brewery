# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import ScreenManager
from screens.activity import Activity
from screens.new_brew import NewBrew
from screens.settings_menu import SettingsMenu
from screens.cooking import Cooking
from screens.main_menu import MainMenu
from screens.new_brew import NewBrew
from screens.saved_configs import SavedConfigs
from screens.save_config import SaveConfig
from screens.edit_hops import EditHops
from screens.finish import Finish

from kivy.lang import Builder

Builder.load_file('layouts/main.kv')

class ScreenManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(ScreenManager, self).__init__(*args, **kwargs)
        self.add_widget(MainMenu(name='MainMenu'))
        self.add_widget(SettingsMenu(name='SettingsMenu'))
        self.add_widget(SavedConfigs(name='SavedConfigs'))
        self.add_widget(Finish(name='Finish'))
        self.add_widget(EditHops(name='EditHops'))
        self.add_widget(NewBrew(name='NewBrew'))
        self.add_widget(Cooking(name='Cooking'))
        self.add_widget(SaveConfig(name='SaveConfig'))
        self.stack = [self.screens[0].name]

    # call when screen is going back to previous screen, possible to pass dictionary with data
    def back(self, data={}):
        self.stack.pop()
        self.get_screen_by_name(self.stack[-1]).on_resume(data)
        self.current = self.stack[-1]

    # call when screen open new screen, possible to pass dictionary with data
    def go(self, name, data={}):
        self.get_screen_by_name(name).on_start(data)
        if name == 'MainMenu':
            self.stack = [name]
        else:
            self.stack.append(name)
        self.current = name
        print(self.stack)

    #  def go_without_snap(self, name, data={}):
    #      self.get_screen_by_name(name).on_start(data)
    #      self.stack.pop()
    #      self.stack.append(name)
    #      self.current = name

    def get_screen_by_name(self, name):
        return next((s for s in self.screens if s.name == name), None)
