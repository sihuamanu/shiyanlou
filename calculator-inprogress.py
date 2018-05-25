#!/usr/bin/env python3

import sys
import csv
import queue
from multiprocessing import Process, Queue
from collections import namedtuple

TAX_START_POINT = 3500

Tax_Quick_Lookup_Items = namedtuple(
    'Quick_Lookup',
    ['start_point', 'tax_rate', 'quick_subtractor']
)

INCOME_QUICK_LOOKUP_ITEMS = [
    Quick_Lookup(80000, 0.45, 13505),
    Quick_Lookup(55000, 0.35, 5505),
    Quick_Lookup(35000, 0.30, 2755),
    Quick_Lookup(9000, 0.25, 1055),
    Quick_Lookup(4500, 0.20, 555),
    Quick_Lookup(1500, 0.10, 105),
    Quick_Lookup(0, 0.03, 0),
]

q_user = Queue()
q_result = Queue()

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    def _value_after_option(self, option):
        try:
            index = self.args.index(option)
            return self.args[index + 1]
        except (ValueError, IndexError):
            print("Parameter Error")
            exit()

    @property
    def config_path(self):
        return _value_ after_option('-c')

    @property
    def userdata_path(self):
        return _value_after_option('d')

    @property
    def export_path(self):
        return _value_after_option('o')

args = Args()

class Config(object):

    def __init__(self):
        self.config = self._read_config() 

    def _read_config(self):
        config_path = args.config_path
        config = {}
        with open(config_path) as file:
            for line in file.readlines():
                key, value = line.strip().split(' = ')
                try:
                    config[key] = float(value)
                except ValueError:
                    print("Parameter Error")
                    exit()
        return config

    def _get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            print("KeyError")
            exit()

    @property
    def social_insurance_baseline_low(self):
        return self._get_config('JiShuL')

    @property
    def social_insurance_baseline_high(self):
        return self._get_config('JiShuH')

    @property
    def social_insurance_total_rate(self):
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('GongShang'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin'),
        ])

config = Config()

class UserData(Process):

    def _read_users_data(self):
        with open(args.userdata_path) as file:
            for line in file.readlines():
                employee_id, income_string = line.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print("Parameter Error")
                    exit()
                yield (employee_id, income)

    def run(self):
        for data in self._read_users_data():
            q_user.put(data)

class IncomeTaxCalculator(Process):

    @staticmethod
    def calc_social_insurance_money(income):
        if income < config.social_insurance_baseline_low:
            return config.social_insurance_baseline_low * \
                config.social_insurance_total_rate
        elif income > config.social_insurance_baseline_high:
            return config.social_insurance_baseline_high * \
                config.social_insurance_total_rate
        else:
            return income * config.social_insurance_total_rate

    @classmethod
    def calc_income_tax_and_remain(cls, income):
        social_insurance_money = cls.calc_social_insurance_money(income)
        real_income = income - social_insurance_money
        tax_part = real_income - TAX_START_POINT
        
