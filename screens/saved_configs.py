# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from screens.activity import Activity
from config_manager import ConfigManager

class SavedConfigs(Screen, Activity):

    class ConfigPosition(Button):
        pass

    def __init__(self, *args, **kwargs):
        super(SavedConfigs, self).__init__(*args, **kwargs)
        # new ConfigManager for read saved configs
        self.config_manager = ConfigManager()

    def on_pre_enter(self):
        # creatin view with positions for every saved config
        positions = self.config_manager.get_list()
        self.ids.config_list.clear_widgets()
        callback = self.choose_config
        get_callback = lambda v: (lambda self: callback(v))
        for name in positions:
            self.ids.config_list.add_widget(
                    self.ConfigPosition(
                        text = name,
                        on_release = get_callback(name),
                    )
                )

    def choose_config(self, name):
        data = self.config_manager.load(name)
        self.manager.go('NewBrew', data)

    def go_to_menu(self):
        self.manager.go('MainMenu')

