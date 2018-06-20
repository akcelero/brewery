# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import Screen
from screens.activity import Activity
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.progressbar import ProgressBar
from kivy.graphics import Color, Rectangle, RoundedRectangle
from confirm_popup import ConfirmPopup
from controler import Controler
from kivy.uix.widget import Widget
from enum import Enum
import time

class Stage(Enum):
    BLURRING_HEATUP = 0
    BLURRING_BREWING = 1
    DESUGARIZATION = 2
    BOILING_HEATING = 3
    BOILING = 4

class StageLabel(Label):
    pass

class CustomProgressBar(Widget):
    border_size = NumericProperty(0)
    val = NumericProperty(100)

    def __init__(self, *args, **kwargs):
        super(CustomProgressBar, self).__init__(*args, **kwargs)

class Cooking(Screen, Activity):
    target_temp = NumericProperty(0)
    current_temp = NumericProperty(0)
    time_left = NumericProperty(0)
    progress = NumericProperty(0)
    pause = BooleanProperty(False)
    pump_block = BooleanProperty(True)
    heaters_block = BooleanProperty(True)

    hops_times = []

    def __init__(self, *args, **kwargs):
        super(Cooking, self).__init__(*args, **kwargs)
        self.controler = Controler()
        # add reaction for emergency switches
        self.ids.pump_block_checkbox.bind(state=lambda _, s: self.controler.block_pump(s == 'down'))
        self.ids.heaters_block_checkbox.bind(state=lambda _, s: self.controler.block_heaters(s == 'down'))

    def loop(self, delta_time=None):
        self.current_temp = self.controler.get_temp()

        if self.pause:
            return

        # these ifs are (mainly) conditions for go to the next stage / substage
        if self.current_stage == Stage.BLURRING_HEATUP:
            self.progress = 0
            if self.controler.temp_reached():
                self.current_stage = Stage.BLURRING_BREWING
                if self.current_level == 0:
                    self.controler.buzzer(2)
                    p = ConfirmPopup()
                    p.set_root(self)
                    p.text = "Temp. osiagnięta.\nDodaj słód"
                    p.font_size_ratio = 0.07
                    p.open()
        elif self.current_stage == Stage.BLURRING_BREWING:
            self.progress = 100 - ((self.time_left * 100) / (self.blurring_config[self.current_level]['time'] * 60))
            self.time_left -= 1
            if self.time_left == 0:
                if self.current_level + 1 < len(self.blurring_config):
                    self.current_level += 1
                    self.time_left = self.blurring_config[self.current_level]['time'] * 60
                    self.target_temp = self.blurring_config[self.current_level]['temp']
                    self.controler.set_temp(self.blurring_config[self.current_level]['temp'])
                    self.current_stage = Stage.BLURRING_HEATUP
                else:
                    self.controler.off()
                    self.current_stage = Stage.DESUGARIZATION
                    self.controler.buzzer(2)
                    p = ConfirmPopup()
                    p.set_root(self)
                    p.text = "Koniec zacierania.\nWysładzanie"
                    p.font_size_ratio = 0.07
                    def start_boiling():
                        self.time_left = 60 * 60
                        self.target_temp = self.controler.TEMP_FOR_CHOPS
                        self.controler.set_temp(self.target_temp)
                        self.current_stage = Stage.BOILING_HEATING
                        self.current_level = 0
                    p.callback = start_boiling
                    p.open()
                    self.controler.buzzer(2)
        elif self.current_stage == Stage.DESUGARIZATION:
            pass
        elif self.current_stage == Stage.BOILING_HEATING:
            self.progress = 0
            if self.controler.temp_reached():
                self.current_stage = Stage.BOILING
        elif self.current_stage == Stage.BOILING:
            self.time_left -= 1
            self.progress = 100 - ((self.time_left * 100) / (60 * 60))
            if self.current_level < len(self.hops_config) and\
                    60 * 60 - self.time_left >= self.hops_config[self.current_level] * 60:
                self.current_level += 1
                p = ConfirmPopup()
                p.set_root(self)
                p.text = "Dodaj chmiel %d" % self.current_level
                p.open()
                self.controler.buzzer(3)
            if self.time_left == 0:
                self.manager.go('Finish')
        else:
            assert False, 'Bad stage ' + str(self.current_stage)

    def on_start(self, data):
        self.blurring_config = data['brewing']
        self.hops_config = data['hops']

    def on_enter(self):
        self.create_stages_list()

    def on_pre_enter(self):
        #  self.loop_schedule = Clock.schedule_interval(self.loop, .05) # debug purposes
        self.loop_schedule = Clock.schedule_interval(self.loop, 1.)
        self.layout_schedule = Clock.schedule_interval(self.update_layout, 1.)
        self.controler_schedule = Clock.schedule_interval(self.controler.update, 1./4.)
        self.update_stage_list = Clock.schedule_interval(self.update_stages_list, 1.)
        self.current_stage = Stage.BLURRING_HEATUP
        self.current_level = 0
        self.time_left = self.blurring_config[self.current_level]['time'] * 60
        self.target_temp = self.blurring_config[self.current_level]['temp']
        self.controler.set_temp(self.target_temp)
        self.pause = False

    def on_pre_leave(self):
        Clock.unschedule(self.loop_schedule)
        Clock.unschedule(self.layout_schedule)
        Clock.unschedule(self.controler_schedule)
        Clock.unschedule(self.update_stage_list)
        self.controler.off()

    def update_layout(self, delta_time=None):
        self.ids.clock.text = self.time()
        etapy = ['ZACIERANIE', 'ZACIERANIE', 'WYSŁADZANIE', 'CHMIEL', 'CHMIEL']
        self.ids.stage_label.text = etapy[self.current_stage.value]
        self.ids.wifi_img.source = 'imgs/wifi%d.png' % (self.controler.get_wifi_range() / 18)

    def inc_temp(self):
        self.target_temp = min(self.target_temp + 1, 300)
        self.controler.set_temp(self.target_temp)

    def dec_temp(self):
        self.target_temp = max(self.target_temp - 1, 0)
        self.controler.set_temp(self.target_temp)

    def eta_time(self, val):
        return time.strftime('%H:%M', time.gmtime(val))

    def time(self):
        return time.strftime('%H:%M')

    def toggle_pause(self):
        self.pause = not self.pause
        dark_blue   = (.21, .23, .35, 1)
        light_blue  = (.51, .53, .65, 1)
        orange      = (.97, .69, .23, 1)
        red         = (1, .0, .0, 1)
        grey        = (.3, .3, .3, 1)
        black       = (.0, .0, .0, 1)
        white       = (1, 1, 1, 1)
        self.ids.pause_button.color = orange if self.pause else dark_blue
        self.ids.pause_button.background_color = grey if self.pause else orange

    def update_stages_list(self, delta_time=None):
        if self.current_stage == Stage.BLURRING_HEATUP:
            index = self.current_level * 2
        elif self.current_stage == Stage.BLURRING_BREWING:
            index = self.current_level * 2 + 1
        elif self.current_stage == Stage.DESUGARIZATION:
            index = len(self.blurring_config) * 2
        elif self.current_stage == Stage.BOILING_HEATING:
            index = len(self.blurring_config) * 2 +\
                    self.current_level + 1
        elif self.current_stage == Stage.BOILING:
            index = len(self.blurring_config) * 2 +\
                    self.current_level + 2
        index = len(self.ids.stages_list.children) - index - 1
        for i, w in enumerate(self.ids.stages_list.children):
            dark_blue   = (.21, .23, .35, 1)
            w.canvas.before.clear()
            if i == index:
                with w.canvas.before:
                    Color(.21, .23, .35, 1)
                    RoundedRectangle(pos=w.pos, size=(w.width * 0.97, w.height),\
                            radius=[(0,0),(20,20),(20,20),(0,0)])
                w.color = (.51, .53, .65, 1)
            else:
                w.color = dark_blue

    # create list of next stages on the right side of screen
    def create_stages_list(self):
        add_record = lambda name: self.ids.stages_list.add_widget(StageLabel(text=name))
        self.ids.stages_list.clear_widgets()
        for item in self.blurring_config:
            add_record('Grzanie')
            add_record('Przerwa ' + str(item['temp']) + "°C")
        add_record('Wysładzanie')
        add_record('Grzanie')
        for time in self.hops_config:
            add_record('Chmiel %dmin' % time)
