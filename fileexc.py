#!/usr/bin/env python3

filename = '/home/shiyanlou/if.py'
f = open(filename)
try:
    f.write('shiyanlou')
except:
    print("File not found")
finally:
    print("finally")
    f.close()
