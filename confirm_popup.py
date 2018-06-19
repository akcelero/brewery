# -*- coding: utf-8 -*-
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.anchorlayout import AnchorLayout

class ConfirmPopup(AnchorLayout):
    text = StringProperty('')
    font_size_ratio = NumericProperty(0.5)

    def set_root(self, root):
        self.root = root

    def open(self):
        self.root.add_widget(self)

    def ok(self):
        self.callback()
        self.root.remove_widget(self)

    def callback(self):
        pass
