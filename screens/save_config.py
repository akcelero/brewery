# -*- coding: utf-8 -*-
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from screens.activity import Activity
from config_manager import ConfigManager

class SaveConfig(Screen, Activity):
    config_manager = ConfigManager()

    def on_start(self, config):
        # pass config for save
        self.config = config

    def on_enter(self):
        # open keyboard
        self._keyboard = Window.request_keyboard(
            None, self.ids.name, 'text')
        self.ids.name.focus = True

    def save(self):
        # save config with name from input
        self.config_manager.save(self.config, self.ids.name.text)
        self.manager.back()

    def leave(self):
        self.manager.back()

