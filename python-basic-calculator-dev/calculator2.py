#!/usr/bin/env python3

import sys

def cal(a, b):
    try:
        income = int(b)
    except ValueError:
        print("Parameter Error")
        exit()
    insurance = income * (0.08 + 0.02 + 0.005 + 0.06)
    tax_income = income - insurance - 3500
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
    post_tax_income = income - insurance - tax_pay
    print( a + ':' +format(post_tax_income, ".2f"))

for i in sys.argv[1:]:
    a, b = i.split(':')
    cal(a, b)
