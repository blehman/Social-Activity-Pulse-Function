#!/usr/bin/env python
import math
import random
import datetime

A = 100
alpha = 0.0025
B = .1
wb = 2*math.pi/(7*24)
C = .2
wc = 2*math.pi/24

starttime = datetime.datetime(2010, 01, 01)

for i in range(10*24*7):
    print starttime +  datetime.timedelta(0, 3600*i), ',', A*math.exp(alpha*i)*(1. + B*math.cos(wb*i) + C*math.cos(wc*i))
