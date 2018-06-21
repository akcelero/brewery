# -*- coding: utf-8 -*-

# class for all screens in this app, for implement passing data between screens during going back or opening new screens

class Activity():
    data = None

    def callback(self, name):
        pass

    def on_start(self, data=None):
        pass

    def on_resume(self, data=None, back_from=None):
        pass

    def back(self):
        pass
