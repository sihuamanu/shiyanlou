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
    Tax_Quick_Lookup_Items(80000, 0.45, 13505),
    Tax_Quick_Lookup_Items(55000, 0.35, 5505),
    Tax_Quick_Lookup_Items(35000, 0.30, 2755),
    Tax_Quick_Lookup_Items(9000, 0.25, 1005),
    Tax_Quick_Lookup_Items(4500, 0.20, 555),
    Tax_Quick_Lookup_Items(1500, 0.10, 105),
    Tax_Quick_Lookup_Items(0, 0.03, 0),
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
            print("Parameter1 Error")
            exit()

    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def export_path(self):
        return self._value_after_option('-o')

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
                    print("Parameter2 Error")
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
        if tax_part < 0:
            return '0.00', '{:.2f}'.format(real_income)
        for item in INCOME_QUICK_LOOKUP_ITEMS:
            if tax_part > item.start_point:
                tax = tax_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income - tax)

    def calc_for_all_userdata(self):
        while True:
            try:
                employee_id, income = q_user.get(timeout=1)
            except queue.Empty:
                return
            data = [employee_id, income]
            social_insurance_money = '{:.2f}'.format(self.calc_social_insurance_money(income))
            tax, remain = self.calc_income_tax_and_remain(income)
            data += [social_insurance_money, tax, remain]
            yield data

    def run(self):
        for data in self.calc_for_all_userdata():
            q_result.put(data)


class Exporter(Process):
    
    def run(self):
        with open(args.export_path, 'w', newline='') as file:
            while True:
                writer = csv.writer(file)
                try:
                    item = q_result.get(timeout=1)
                except queue.Empty:
                    return
                writer.writerow(item)


if __name__ == '__main__':
    workers = [
        UserData(),
        IncomeTaxCalculator(),
        Exporter() 
    ]
    for worker in workers:
        worker.run()
