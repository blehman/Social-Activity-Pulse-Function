#!/usr/bin/env python
import sys
import csv
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--column",  dest="column", default=2,
                help="Column to scale (default is 2)")
parser.add_option("-t", "--time",  dest="time", default=None,
                help="Scale the time column to start at zero (new time in first column)")
(options, args) = parser.parse_args()

idx = int(options.column) - 1
tidx = None
if options.time is not None:
    tidx = int(options.time) - 1

wrt = csv.writer(sys.stdout)
data = []
first = True
maxx = -sys.maxint
minx = sys.maxint
for x in csv.reader(sys.stdin):
    try:
        tmp = float(x[idx])
        if first and options.time is not None:
            t0 = float(x[tidx])
            first = False
        data.append(x)
        if tmp > maxx:
            maxx = tmp
        if tmp < minx:
            minx = tmp
    except:
        x.insert(idx+1, "val_scale")
        if options.time is not None:
            x.insert(0,"time_scale")
        wrt.writerow(x)

for x in data:
    x.insert(idx+1, (float(x[idx])-minx)/(maxx-minx))
    if tidx is not None:
        delta = 0
        if tidx > idx:
            delta = 1
        x.insert(0, float(x[tidx + delta]) - t0)
    wrt.writerow(x)
