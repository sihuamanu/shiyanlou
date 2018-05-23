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
            try:
                for i in l:
                    a, b = i.split('=')    
                    config[a.strip()] = float(b)
            except:
                print("Error")
                exit()
            return config

class UserData(object):

    def __init__(self):
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        userdata = []
        filename = Args().userdata
        with open(filename) as file:
            l = file.readlines()
            try:
                for i in l:
                    a, b = i.split(',')
                    userdata.append((a.strip(), int(b)))
                return userdata
            except:
                print("Error")

def IncomeTaxCalculator(object):

    def calc_for_all_userdata(self):
        

args = Args()
print(args.configfile)
print(args.userdata)
print(args.output)
config = Config()
print(config.config)
userdata = UserData()
print(userdata.userdata)
