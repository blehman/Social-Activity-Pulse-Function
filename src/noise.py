#!/usr/bin/env python
import sys
import csv
import random
var = 0.15
idx = 1
scale = 100
wrt = csv.writer(sys.stdout)
for x in csv.reader(sys.stdin):
    try:
        val = float(x[idx])
        delta= 2.*val*var*(random.random()-0.5)
        x[idx] = 100*(val + delta)
        #print x, val, delta
    except TypeError:
        pass
    except IndexError:
        pass
    wrt.writerow(x)
