#!/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import FadeTransition
from kivy.garden.knob import  Knob
from kivy.config import Config
from screen_manager import ScreenManager

Builder.load_file('layouts/main.kv')


class MainApp(App):
    sm = ScreenManager(transition=FadeTransition());
    def build(self):
        return self.sm


if __name__ == "__main__":
    Window.show_cursor = True
    Window.allow_vkeyboard = True
    Window.fullscreen = False

    Config.set("kivy", "keyboard_mode", "dock")
    Config.set("graphics", "show_cursor", 1)
    Config.write()
    MainApp().run()
