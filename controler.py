# -*- coding: utf-8 -*-
from time import sleep
from kivy.clock import Clock
import threading
#  from concurrent.futures import ThreadPoolExecutor
import os
rpi_platform = os.uname()[4].startswith('arm')
if rpi_platform:
    from w1thermsensor import W1ThermSensor
    import wiringpi
    sensor = W1ThermSensor()
else:
    from unittest.mock import MagicMock, Mock
    def measure():
        with open('temp') as f:
            return int(f.read())
    wiringpi = MagicMock()
    sensor = MagicMock()
    sensor.get_temperature = Mock(side_effect=measure)


class Controler():
    current_temp = 0
    target_temp = -100
    temp_delta = 0
    temp = 0
    BUZZER_PIN = 3
    SMALL_HEATER_PIN = 2
    BIG_HEATER_PIN = 7
    PUMP_PIN = 8
    heaters_block = False
    pump_block = False
    dbg = {'pump': 1, 'small heater': 1, 'big heater': 1}

    # IMPORTANT
    # big and small heater and also pump can't be turn on in the same time (probably because high power consumption)
    # so there are object of scheduled events for turning on big heater and another for turning on pump
    # small heater can be turn on immediately without delay
    big_on_schedule = None
    pump_on_schedule = None

    PUMP_TEMP_LIMIT = 50 # 95
    TEMP_FOR_CHOPS = 60 # 100

    def __init__(self):
        # set GPIOs modes
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.SMALL_HEATER_PIN, 1)
        wiringpi.pinMode(self.BIG_HEATER_PIN, 1)
        wiringpi.pinMode(self.PUMP_PIN, 1)
        wiringpi.pinMode(self.BUZZER_PIN, 1)
        wiringpi.digitalWrite(self.BUZZER_PIN, 1)
        # just in case turn off heaters and pump
        self.off()
        # create thread for reading temp without stoping main thread
        self.reading_thread = threading.Thread(name='reading sensor', target=self.read_temp)
        self.reading_thread.start()

    def get_temp(self):
        # giving last measured temperature
        if not self.reading_thread.isAlive():
            self.reading_thread = threading.Thread(name='reading sensor', target=self.read_temp)
            self.reading_thread.start()
        return self.temp

    def read_temp(self):
        # method for thread that measure temperature from sensor
        self.temp = round(sensor.get_temperature())

    def update(self, detla_time=None):
        # method for turn on/off peripherals for keep target temperature
        # this method also take care about emergency switch
        self.current_temp = self.get_temp()

        if self.current_temp < self.target_temp:
            if not self.heaters_block:
                self.small_heater(True)
                if self.big_on_schedule == None:
                    self.big_on_schedule = Clock.schedule_once(lambda delta: self.big_heater(True), 0.5)
                else:
                    self.big_on_schedule()
            else:
                self.small_heater(False)
                self.big_heater(False)
            if self.target_temp < self.PUMP_TEMP_LIMIT and not self.pump_block:
                if self.pump_on_schedule == None:
                    self.pump_on_schedule = Clock.schedule_once(lambda delta: self.pump(True), 1)
                else:
                    self.pump_on_schedule()
            else:
                self.pump(False)
        else:
            self.small_heater(False)
            self.big_heater(False)
            self.pump(False)

    # next 2 methods are for emergency switch peripherals
    def block_heaters(self, block):
        if block and self.big_on_schedule != None:
            self.big_on_schedule.cancel()
        self.heaters_block = block

    def block_pump(self, block):
        if block and self.pump_on_schedule != None:
            self.pump_on_schedule.cancel()
        self.pump_block = block

    def debug(self, delta_time=None):
        print("(%d : %d)(%d) : %d(%d) %d/%d" % (self.dbg['big heater'], self.dbg['small heater'], int(self.heaters_block), self.dbg['pump'], int(self.pump_block), int(self.target_temp), int(self.current_temp)))

    def set_temp(self, temp):
        self.target_temp = temp

    def temp_reached(self):
        self.temp_delta = 2
        return (self.target_temp - self.temp_delta) <= self.current_temp <= (self.target_temp + self.temp_delta)

    def buzzer(self, time):
        # method turn on buzzer and also set turn off after given amount of seconds
        wiringpi.digitalWrite(self.BUZZER_PIN, 0)
        Clock.schedule_once(lambda delta: wiringpi.digitalWrite(self.BUZZER_PIN, 1), time)

    def pump(self, power):
        if self.pump_on_schedule != None:
            self.pump_on_schedule.cancel()
        if power and not self.pump_block:
            wiringpi.digitalWrite(self.PUMP_PIN, 0)
            self.dbg['pump'] = 0
        else:
            wiringpi.digitalWrite(self.PUMP_PIN, 1)
            self.dbg['pump'] = 1

    def small_heater(self, power):
        if power and not self.heaters_block:
            wiringpi.digitalWrite(self.SMALL_HEATER_PIN, 0)
            self.dbg['small heater'] = 0
        else:
            wiringpi.digitalWrite(self.SMALL_HEATER_PIN, 1)
            self.dbg['small heater'] = 1

    def big_heater(self, power):
        if self.big_on_schedule != None:
            self.big_on_schedule.cancel()
        if power and not self.heaters_block:
            wiringpi.digitalWrite(self.BIG_HEATER_PIN, 0)
            self.dbg['big heater'] = 0
        else:
            wiringpi.digitalWrite(self.BIG_HEATER_PIN, 1)
            self.dbg['big heater'] = 1

    def off(self):
        self.target_temp = -100
        if self.pump_on_schedule:
            self.pump_on_schedule.cancel()
        if self.big_on_schedule:
            self.big_on_schedule.cancel()
        self.small_heater(False)
        self.big_heater(False)
        self.pump(False)

    def get_wifi_range(self):
        interfaces = [l for l in open('/proc/net/wireless').readlines()]
        if len(interfaces) < 3:
            return 0
        return int(float(interfaces[2].split()[2]))
