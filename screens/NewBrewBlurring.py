from kivy.uix.screenmanager import Screen
from screens.Activity import Activity
from config_manager import ConfigManager
import datetime

class NewBrewBlurring(Screen, Activity):

    def __init__(self, *args, **kwargs):
        super(NewBrewBlurring, self).__init__(*args, **kwargs)
        self.test = 0
        self.ids.temp_zacierania_knob.on_knob = self.on_knob_temp
        self.ids.czas_zacierania_knob.on_knob = self.on_knob_czas
        self.conf=[{'temp': 20, 'time': 15}]
        self.update_layout()
        self.config_manager = ConfigManager()

    def on_resume(self, conf=None):
        if conf:
            self.conf = conf
            self.update_layout()

    def on_start(self, conf=None):
        if conf:
            self.conf = conf
            self.update_layout()

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
        self.manager.go('Cooking', self.conf)

    def on_knob_temp(self, val):
        self.conf[-1]['temp'] = int(val)
        self.update_layout()

    def on_knob_czas(self, val):
        self.conf[-1]['time'] = int(val)
        self.update_layout()

    def update_layout(self):
        time = self.conf[-1]['time']
        temp = self.conf[-1]['temp']
        self.ids.czas_zacierania_label.text = str(time) + "min"
        self.ids.temp_zacierania_label.text = str(temp) + "°C"
        self.ids.podetap_label.text = "PODETAP " + str(len(self.conf))
        d = datetime.datetime.now()
        self.ids.date.text = ("%d-%d-%d" % (d.day, d.month, d.year))

    def next_stage(self):
        self.conf.append({'temp': 20, 'time': 15})
        self.update_layout()

    def prev_stage(self):
        self.conf = self.conf[:-1]
        if len(self.conf) == 0:
            self.conf.append({'temp': 20, 'time': 15})
        self.update_layout()

    def inc_temp(self):
        self.conf[-1]['temp'] = (self.conf[-1]['temp'] + 1) % 100
        self.update_layout()

    def dec_temp(self):
        self.conf[-1]['temp'] = (self.conf[-1]['temp'] + 99) % 100
        self.update_layout()

    def save_config(self):
        self.manager.go('SaveConfig', self.conf)
