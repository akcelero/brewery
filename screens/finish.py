# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from screens.activity import Activity

class Finish(Screen, Activity):

    def go_to_menu(self):
        self.manager.go('MainMenu')
