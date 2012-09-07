#!/usr/bin/env python
import math
import random
import datetime

A = 100
alpha = 0.0009
B = .05/2.
wb = 2*math.pi/(7*24)
C = .1/2.
#C = 100
wc = 2*math.pi/24

starttime = datetime.datetime(2010, 01, 01)

for i in range(25*24*7):
    t = starttime +  datetime.timedelta(0, 3600*i)
    val = A*math.exp(alpha*i)*(1. + B*(1.+math.cos(wb*i)) + C*(1.+math.cos(wc*i)))
    event = 0
    if i == 621 or i == 624:
        event = 100
    print ','.join([str(t), str(val), str(val + event)])
