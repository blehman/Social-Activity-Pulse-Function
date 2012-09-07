#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import numpy
import datetime
import re
import sys
import exp_function
import function_fit

fmtStr = "%Y-%m-%d %H:%M:%S"

class timeseries_decompose(object):
    def __init__(self, data):
        # data is datestring, timestamp, value
        # shift epoch for exp fit and count by hours
        epoch = data[0][1]
        self.data = [ [datetime.datetime.strptime(d[0], fmtStr), (d[1]-epoch)/3600., d[2], 0, 0, 0] for d in data ]
        self.fitExp(2,3)
        #self.dowFactors()
        self.hodFactors(3,4)
        self.howFactors(3,5)

    def fitExp(self, src, dest):
        # sets column index 3
        tmp = []
        for d in self.data:
            tmp.append((d[1],d[src]))  # ts, value    
        ef = function_fit.function_fit(tmp, exp_function.func())
        sys.stderr.write(str(ef.fit()))
        for d in self.data:
            d[dest] = d[src] - ef.f.eval(d[1])[0]

    def dowFactors(self, src, dest):
        # sets column index 4
        counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0 }
        for d in self.data:
            counts[d[0].weekday()] += d[src]
        #avgDay = sum(counts.values())/7.
        avgDay = len(self.data)/7.
        for d in self.data:
            d[dest] = avgDay * d[src]/counts[d[0].weekday()]

    def hodFactors(self, src, dest):
        counts = {}
        for i in range(24):
            counts[i] = 0
        for d in self.data:
            counts[d[0].hour] += d[src]
        #avgHour = sum(counts.values())/24.
        avgHour = len(self.data)/24.
        for d in self.data:
            d[dest] = avgHour * d[src]/counts[d[0].hour]

    def howFactors(self, src, dest):
        counts = {}
        for i in range(24*7):
            counts[i] = 0
        for d in self.data:
            counts[self.hourOfWeek(d[0])] += d[src]
        #avgHour = sum(counts.values())/24.
        avgHour = len(self.data)/(7.*24.)
        for d in self.data:
            d[dest] = avgHour * d[src]/counts[self.hourOfWeek(d[0])]

    def hourOfWeek(self, dt):
        # date time to hour of week
        return int(dt.weekday() * 24 + dt.hour)

    def csv(self):
        print "date, ts, original, detrended, weekly, daily"
        for d in self.data:
            print ','.join([str(x) for x in d])

    def signal(self):
        for d in self.data:
            yield [d[0], d[5]]
