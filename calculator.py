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
                exit()

class IncomeTaxCalculator(object):

    def calc_for_all_userdata(self):
        user = UserData().userdata
        config = Config().config
        coefficient = (config['YangLao'] + config['YiLiao'] + config['ShiYe'] + config['GongShang'] + config['ShengYu'] + config['GongJiJin'])
        basenum = 3500
        resultList = []
        for i in user:
            if i[1] < config['JiShuL']:
                insurance = config['JiShuL'] * coefficient  
            elif i[1] > config['JiShuH']:
                insurance = config['JiShuH'] * coefficient
            else:
                insurance = i[1] * coefficient
            tax_income = i[1] - insurance - basenum
            if tax_income <= 0:
                tax_pay = 0
            elif tax_income <= 1500:
                tax_pay = tax_income * 0.03 - 0
            elif tax_income <= 4500:
                tax_pay = tax_income * 0.10 - 105
            elif tax_income <= 9000:
                tax_pay = tax_income * 0.20 - 555
            elif tax_income <= 35000:
                tax_pay = tax_income * 0.25 - 1005
            elif tax_income <= 55000:
                tax_pay = tax_income * 0.30 - 2755
            elif tax_income <= 80000:
                tax_pay = tax_income * 0.35 - 5505
            else:
                tax_pay = tax_income * 0.45 - 13505
            post_tax_income = i[1] - insurance - tax_pay
            resultList.append((i[0],i[1],format(insurance, ".2f"),format(tax_pay, ".2f"),format(post_tax_income, ".2f")))
        return resultList 

    def export(self, default='csv'):

        result = self.calc_for_all_userdata()
        with open(Args().output, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(result)

if __name__ == '__main__':   

    calpay = IncomeTaxCalculator()
    calpay.calc_for_all_userdata()
    calpay.export()
