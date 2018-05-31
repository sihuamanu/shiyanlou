#!/usr/bin/env python3

import sys

try:
    income = int(sys.argv[1])
except ValueError:
    print("Parameter Error")

tax_income = income - 3500

if tax_income <= 1500:
    tax_pay = tax_income * 0.03 - 0
    print(format(tax_pay, ".2f"))
elif tax_income <= 4500:
    tax_pay = tax_income * 0.10 - 105
    print(format(tax_pay, ".2f"))
elif tax_income <= 9000:
    tax_pay = tax_income * 0.20 - 555
    print(format(tax_pay, ".2f"))
elif tax_income <= 35000:
    tax_pay = tax_income * 0.25 - 1005
    print(format(tax_pay, ".2f"))
elif tax_income <- 55000:
    tax_pay = tax_income * 0.30 - 2755
    print(format(tax_pay, ".2f"))
elif tax_income <= 80000:
    tax_pay = tax_income * 0.35 - 5505
    print(format(tax_pay, ".2f"))
else:
    tax_pay = tax_income * 0.45 - 13505
    print(format(tax_pay, ".2f"))
