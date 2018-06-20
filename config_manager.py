# -*- coding: utf-8 -*-
import pickle
import json
import os

class ConfigManager():

    def save(self, config, name ):
        with open('configs/'+ name + '.js', 'w') as f:
            json.dump(config, f)
            return True
        return False

    def load(self, name):
        with open('configs/' + name + '.js', 'r') as f:
            return json.load(f)
        return None

    def get_list(self):
        return sorted([f.split('.')[0] for f in os.listdir("configs") if f.endswith('.js')])
