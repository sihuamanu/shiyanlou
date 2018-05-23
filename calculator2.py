#!/usr/bin/env python3

import sys
import os
import csv

class Args(object):
    
    def __init__(self):
        self.args = sys.argv[1:]
        try:                
            index = self.args.index('-c')
            self.configfile = self.args[index+1]
            index = self.args.index('-d')
            self.userdata = self.args[index+1]
            index = self.args.index('-o')
            self.output = self.args[index+1]
        except:
            print("Error")
            exit()

class Config(object):
    
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config = {}
        filename = Args().configfile
        with open(filename) as file:
            l = file.readlines()
            for i in l:
                a, b = i.split('=')    
                config = {a.strip():b.strip()}
                return config



args = Args()
print(args.configfile)
print(args.userdata)
print(args.output)
config = Config()
print(config.config)
