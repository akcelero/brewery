from kivy.uix.screenmanager import Screen
from screens.Activity import Activity
from kivy.clock import Clock
import time

class Cooking(Screen, Activity):

    def __init__(self, *args, **kwargs):
        super(Cooking, self).__init__(*args, **kwargs)
        self.current_stage = 0
        self.target_temp = 20

    def schedule_loop(self):
        self.loop_schedule = Clock.schedule_interval(self.loop,1/2.)

    def unschedule_loop(self):
        Clock.unschedule(self.loop_schedule)

    def loop(self, time=None):
        self.update_layout()
        current_time = int(time.time())
        current_delay = self.config[self.current_stage]['time'] * 60
        self.time_left = self.time_start + current_delay - current_time
        if self.time_left <= 0:
            current_stage += 1
        if len(self.config) == current_stage:
            self.unschedule_loop()



    def on_start(self, data):
        print(data)
        self.time_start = int(time.time())
        self.current_stage = 0
        self.config = data
        self.schedule_loop()

    def go_to_menu(self):
        self.unschedule_loop()
        self.manager.go('MainMenu')

    def go_to_finish(self):
        #@TODO: IMPLEMENT
        pass

    def update_layout(self):
        #  self.ids.time.text = time.strftime('%H:%M:%S')
        self.ids.time.text = time.strftime('%H:%M')
        self.ids.target_temp1.text = '%d°C' %self.target_temp
        self.ids.target_temp2.text = '%d°C' %self.target_temp
        self.ids.etap_label.text = "ETAP %d" % (self.current_stage + 1)
        self.ids.eta.text = time.strftime('%H:%M:%S', time.gmtime(self.time_left))

    def inc_temp(self):
        self.target_temp = min(self.target_temp + 1, 100)
        self.update_layout()

    def dec_temp(self):
        self.target_temp = max(self.target_temp - 1, 0)
        self.update_layout()
