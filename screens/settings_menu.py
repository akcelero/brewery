# -*- coding: utf-8 -*-
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from screens.activity import Activity
from kivy.config import Config

class SettingsMenu(Screen, Activity):
    rotation_prop = StringProperty('down')

    def __init__(self, *args, **kwargs):
        super(SettingsMenu, self).__init__(*args, **kwargs)
        # setting switch in good position
        self.rotation_prop = 'down' if Config.getint("graphics", "rotation") == 0 else 'normal'
        self.ids.rotation_checkbox.bind(state=self.rotate)

    # this setting is permanent for all kivy apps
    def rotate(self, item, value):
        Config.set("graphics", "rotation", 0 if value == 'down' else 180)
        Config.write()

    def go_to_menu(self):
        self.manager.back()
