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


Builder.load_file('layouts/main.kv')

class Activity():
    def callback(self, name):
        pass

    def on_start(self, name):
        pass

    def on_resume(self, name):
        self.callback(name)

    def back(self):
        self.manager.back()


class ScreenManagement(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(ScreenManagement, self).__init__(*args, **kwargs)
        self.screens = [
                Cooking(name='Cooking'),
                MainMenu(name='MainMenu'),
                NewBrewBlurring(name='NewBrewBlurring'),
            ]
        [self.add_widget(self.screens[i]) for i in range(len(self.screens))]
        self.stack = [self.screens[0].name]

    def back(self):
        name = self.stack[-1]
        self.stack = self.stack[:-1]
        self.get_screen_by_name(self.stack[-1]).on_resume(name)
        self.current = self.stack[-1]

    def go(self, name):
        self.get_screen_by_name(name).on_start(self.stack[-1])
        self.current = name
        if name == 'MainMenu':
            self.stack = [name]
        else:
            self.stack.append(name)

    def get_screen_by_name(self, name):
        return next((s for s in self.screens if s.name == name), None)


class Cooking(Screen, Activity):
    def menu(self):
        self.manager.go('MainMenu')

class NewBrewBlurring(Screen, Activity):

    def __init__(self, *args, **kwargs):
        super(NewBrewBlurring, self).__init__(*args, **kwargs)
        self.test = 0
        self.ids.temp_zacierania_knob.on_knob = self.on_knob_temp
        self.ids.czas_zacierania_knob.on_knob = self.on_knob_czas

    def on_start(self, name):
        pass
        #  self.ids.wartosc.text = '0'

    def edit_val(self, name):
        if name == 'NumberInput':
            self.ids.wartosc.text = str(self.manager.get_screen_by_name('NumberInput').result)

    def get_num(self):
        self.manager.get_screen_by_name('NumberInput').set_result(self.test)
        self.manager.go('NumberInput')
        self.callback = self.edit_val

    def menu(self):
        self.manager.go('MainMenu')

    def cooking(self):
        self.manager.go('Cooking')

    def on_knob_temp(self, val):
        self.ids.temp_zacierania_label.text = str(int(val)) + "°C"

    def on_knob_czas(self, val):
        self.ids.czas_zacierania_label.text = str(int(val)) + "min"


class MainMenu(Screen, Activity):

    def newBrew(self):
        self.manager.go('NewBrewBlurring')


class MainApp(App):
    sm = ScreenManagement(transition=FadeTransition());
    def build(self):
        return self.sm


if __name__ == "__main__":
    MainApp().run()
