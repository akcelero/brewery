# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from screens.activity import Activity
from kivy.properties import NumericProperty

class Chmiel(BoxLayout):
    time = NumericProperty(0)
    number = NumericProperty(0)

    # buttons became pushed
    def inc_pressed(self):
        self.time += 1
        self.inc_schedule = Clock.schedule_once(self.inc, 0.7)

    def dec_pressed(self):
        self.time -= 1
        self.dec_schedule = Clock.schedule_once(self.dec, 0.7)

    # buttons realeased
    def inc_released(self):
        Clock.unschedule(self.inc_schedule)

    def dec_released(self):
        Clock.unschedule(self.dec_schedule)

    # buttons during being pushed
    def inc(self, delta_time=None):
        self.time += 1
        self.inc_schedule = Clock.schedule_once(self.inc, 0.1)

    def dec(self, delta_time=None):
        self.time -= 1
        self.dec_schedule = Clock.schedule_once(self.dec, 0.1)


class EditHops(Screen, Activity):

    # set times
    times = [0, 0, 0]
    # widgets for display
    hops = []

    def __init__(self, *args, **kwargs):
        super(EditHops, self).__init__(*args, **kwargs)

    def on_start(self, conf=None):
        print(conf)
        if conf:
            # no list comprehension, bacase there needs to be 3 options, independ on variable conf
            for i, time in enumerate(conf):
                self.times[i] = time

    def on_pre_enter(self):
        # add positions with specified values
        self.ids.input_list.clear_widgets()
        self.hops = [Chmiel() for _ in self.times]
        [self.ids.input_list.add_widget(hop) for hop in self.hops]
        for hop, time, i in zip(self.hops, self.times, range(len(self.times))):
            hop.time = time
            hop.number = i
            hop.id = 'hop%d' % i

    def accept(self):
        # read and return set values
        res = [hop.time for hop in self.hops if hop.time != 0]
        self.manager.back(res)
