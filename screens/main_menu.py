# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from screens.activity import Activity

class MainMenu(Screen, Activity):

    def settings(self):
        self.manager.go('SettingsMenu')

    def new_brew(self):
        self.manager.go('NewBrew')

    def saved_configs(self):
        self.manager.go('SavedConfigs')
