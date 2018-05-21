from kivy.uix.screenmanager import Screen
from screens.Activity import Activity
from config_manager import ConfigManager

class SaveConfig(Screen, Activity):

    def __init__(self, *args, **kwargs):
        super(SaveConfig, self).__init__(*args, **kwargs)
        self.config_manager = ConfigManager()

    def on_start(self, config):
        self.config = config

    def save(self):
        self.config_manager.save(self.config, self.ids.name.text)
        self.manager.back()

