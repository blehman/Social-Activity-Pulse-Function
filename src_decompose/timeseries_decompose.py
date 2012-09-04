#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import numpy
import datetime
import re
import exp_function
import function_fit

fmtStr = "%Y-%m-%d %H:%M:%S"

class timeseries_decompose(object):
    def __init__(self, data):
        # data is datestring, timestamp, value
        self.data = [ [datetime.datetime.strptime(d[0], fmtStr), d[1], d[2], 0, 0, 0] for d in data ]
        self.csv()
        self.fitExp()
        self.dowFactors()
        self.hodFactors()


    def fitExp(self):
        # sets column index 3
        tmp = []
        for d in self.data:
            tmp.append((d[1],d[2]))  # ts, value    
        ef = function_fit.function_fit(tmp, exp_function.func())
        print str(ef.fit())
        for d in self.data:
            d[3] = d[2] - ef.eval(d[1])

        
    def dowFactors(self):
        # sets column index 4
        counts = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0 }
        for d in self.data:
            counts[d[0].weekday()] += d[3]
        avgDay = sum(counts.values())/7.
        dowF = {}
        for c in counts:
            dowF[c] = float(counts)/avgDay
        for d in self.data:
            d[4] = d[3]/dowF[d[0].weekday()]

    def dowFactors(self):
        counts = {}
        for i in range(24):
            counts[i] = 0
        for d in self.data:
            counts[d[0].hour] += d[4]
        avgHour = sum(counts.values())/24.
        dohF = {}
        for c in counts:
            dohF[c] = float(counts)/avgHour
        for d in self.data:
            d[5] = d[4]/dohF[d[0].hour]
           

    def csv(self):
        for d in self.data:
            print ','.join([str(x) for x in d])

    def detrendedData(self):
        for d in self.data:
            yield [d[0], d[1], d[5]]
