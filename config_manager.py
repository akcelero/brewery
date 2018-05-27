# -*- coding: utf-8 -*-
import pickle
import os

class ConfigManager():

    def save(self, config, name ):
        with open('configs/'+ name + '.pkl', 'wb') as f:
            pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)
            return True
        return False

    def load(self, name):
        with open('configs/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    def get_list(self):
        return [f.split('.')[0] for f in os.listdir("configs")]
