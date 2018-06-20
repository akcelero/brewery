# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from screens.activity import Activity
from config_manager import ConfigManager
from confirm_popup import ConfirmPopup
from kivy.properties import NumericProperty
from kivy.clock import Clock
from controler import Controler
import datetime

class NewBrew(Screen, Activity):
    temp = NumericProperty(0)
    MAX_TEMP = NumericProperty(300)

    def __init__(self, *args, **kwargs):
        super(NewBrew, self).__init__(*args, **kwargs)
        self.test = 0
        self.ids.temp_zacierania_knob.on_knob = self.on_knob_temp
        self.ids.mashing_time_knob.on_knob = self.on_knob_time
        self.conf=[{'temp': 20, 'time': 15}]
        self.update_layout()
        self.config_manager = ConfigManager()
        self.hops_amount = 3
        self.hops = []
        self.controler = Controler()

    def on_resume(self, conf=None):
        # in default this is called just when going back from editing hops
        self.hops = conf

    def on_start(self, conf=None):
        # set parameters from passed config
        if conf:
            self.conf = conf['brewing']
            self.hops = conf['hops']
            self.update_layout()

    def on_pre_enter(self):
        def temp_update(delta_time=None):
            self.temp = self.controler.get_temp()
        self.temp_schedule = Clock.schedule_interval(temp_update, 1.)

    def on_pre_leave(self):
        Clock.unschedule(self.temp_schedule)

    def menu(self):
        self.manager.go('MainMenu')

    def cooking(self):
        # shows info (add water) before go cooking
        p = ConfirmPopup()
        p.set_root(self)
        p.text = 'WLEJ WODĘ'
        cooking_data = {'brewing': self.conf, 'hops': self.hops}
        p.callback = lambda: self.manager.go('Cooking', cooking_data)
        p.open()

    # on move knob
    def on_knob_temp(self, val):
        self.conf[-1]['temp'] = int(val)
        self.update_layout()

    def on_knob_time(self, val):
        self.conf[-1]['time'] = int(val)
        self.update_layout()

    # it hasn't done by properties because conf is array, this method is much clearer
    def update_layout(self):
        time = self.conf[-1]['time']
        temp = self.conf[-1]['temp']
        self.ids.mashing_time_label.text = str(time) + "min"
        self.ids.temp_zacierania_label.text = str(temp) + "°C"
        self.ids.podetap_label.text = "PODETAP " + str(len(self.conf))
        d = datetime.datetime.now()
        self.ids.date.text = ("%d-%d-%d" % (d.day, d.month, d.year))

    def go_to_edit_hops(self):
        self.manager.go('EditHops', self.hops)

    def next_stage(self):
        self.conf.append({'temp': 20, 'time': 15})
        self.update_layout()

    def prev_stage(self):
        if len(self.conf) > 1:
            self.conf = self.conf[:-1]
        self.update_layout()

    # use for plus and minus signs
    def inc_temp(self):
        self.conf[-1]['temp'] = (self.conf[-1]['temp'] + 1 % self.MAX_TEMP)
        self.update_layout()

    def dec_temp(self):
        self.conf[-1]['temp'] = (self.conf[-1]['temp'] - 1 % self.MAX_TEMP)
        self.update_layout()

    def save_config(self):
        data = {'brewing': self.conf, 'hops': self.hops}
        self.manager.go('SaveConfig', data)
