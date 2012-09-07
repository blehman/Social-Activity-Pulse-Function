#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import numpy
import datetime
import re
import sys
import math
import exp_function
import lin_function
import parlin_function
import function_fit

fmtStr = "%Y-%m-%d %H:%M:%S"
outliers = 3

class timeseries_decompose(object):
    def __init__(self, data):
        # data is datestring, timestamp, value
        # shift epoch and count by hours (exp fit)
        epoch = data[0][1]
        self.data = [ [datetime.datetime.strptime(d[0], fmtStr), (d[1]-epoch)/3600., d[2], 0, 0, 0] for d in data ]
        #self.fitExp(2,3)
        self.fitExp(2,3,b=0.000314)
        #self.dowFactors(3,4)
        self.hodFactors(3,4)
        self.howFactors(3,5)

    def fitExp(self, src, dest, b=None):
        tmp = []
        for d in self.data:
            if d[src] > 0:
                tmp.append((d[1],math.log(d[src])))  # ts, value    
        if b is None:
            ef = function_fit.function_fit(tmp, lin_function.func())
        else:
            ef = function_fit.function_fit(tmp, parlin_function.func(_m=b))
        sys.stderr.write("%s\n"%str(ef.fit()))
        [b, a] = ef.f.getParList()
        A = math.exp(a)
        for d in self.data:
            d[dest] = d[src] - A*math.exp(b * d[1])

    def dowFactors(self, src, dest):
        counts = {i:[] for i in range(7)}
        for d in self.data:
            counts[d[0].weekday()].append(d[src])
        avgs = {i:numpy.average(sorted(counts[i])[outliers:-outliers]) for i in counts}
        for d in self.data:
            d[dest] = d[src]/avgs[d[0].weekday()]

    def hodFactors(self, src, dest):
        counts = {i:[] for i in range(24)}
        for d in self.data:
            counts[d[0].hour].append(d[src])
        avgs = {i: numpy.average(sorted(counts[i])[outliers:-outliers]) for i in counts}
        for d in self.data:
            d[dest] = d[src]/avgs[d[0].hour]

    def howFactors(self, src, dest):
        counts = {i:[] for i in range(7*24)}
        for d in self.data:
            counts[self.hourOfWeek(d[0])].append(d[src])
        avgs = {i: numpy.average(sorted(counts[i])[outliers:-outliers]) for i in counts}
        for d in self.data:
            d[dest] = d[src]/avgs[self.hourOfWeek(d[0])]

    def hourOfWeek(self, dt):
        # date time to hour of week
        return int(dt.weekday() * 24 + dt.hour)

    def csv(self):
        print "date, ts, Original,Detrended,HourOfDay,HourOfWeek"
        for d in self.data:
            print ','.join([str(x) for x in d])

    def signal(self):
        for d in self.data:
            yield [d[0], d[5]]
