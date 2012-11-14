#!/usr/bin/env python
import sys
import csv
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--column",  dest="column", default=2,
                help="Column to scale (default is 2)")
(options, args) = parser.parse_args()

idx = int(options.column) - 1
wrt = csv.writer(sys.stdout)
data = []
maxx = -sys.maxint
minx = sys.maxint
for x in csv.reader(sys.stdin):
    try:
        tmp = float(x[idx])
        data.append(x)
        if tmp > maxx:
            maxx = tmp
        if tmp < minx:
            minx = tmp
    except:
            wrt.writerow(x[:idx] + ["scale"] + x[idx:])

for x in data:
    wrt.writerow(x[:idx+1] + [(float(x[idx])-minx)/(maxx-minx)] + x[idx+1:])
