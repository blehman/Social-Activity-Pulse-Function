#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
import math
import numpy
import sys
from base_function import base_function

class func(base_function):
    """ This is the exponential function and associated utilities for evaluating and fitting. """
    def __init__(self, _a = 1., _A0 = 1.):
        self.a = float(_a)
        self.A0 = float(_A0)

    def eval(self, x, baseline=None):
        return [self.A0 * math.exp(self.a * x)]

    def setParList(self, par):
        [self.a, self.A0] = par

    def getParList(self):
        return [self.a, self.A0]

    def nonZeroVec(self, n, l):
        res = []
        cnt = 0
        if n < 0:
            l.reverse()
        for x in l:
            if x != 0:
                res.append(x)
                cnt +=1
            if cnt >= n:
                return res
        
    def guessFromData(self, x, y):
        l = int(0.1*len(x))
        y1 = numpy.average(numpy.log(self.nonZeroVec(-l, y)))
        y0 = numpy.average(numpy.log(self.nonZeroVec(l, y)))
        a = (math.log(y[-1]) - math.log(y[0]))/(x[-1] - x[0])
        A = y[0]
        return [a, A]

    # Output
    def __repr__(self):
        res = "\n#  a=%f\n#  A0=%f"%tuple(self.getParList())
        return res

#########################
if __name__ == '__main__':
    # simple demos
    pf = func(_a=-0.1, _A0=5)
    pf.printPoints(10, 18.)
    print pf
