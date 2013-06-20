#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
import math
import numpy
import sys
from base_function import base_function

class func(base_function):
    """ This is the PARTIAL linear function (slope held constant, best fit to intercept
    and associated utilities for evaluating and fitting. """
    def __init__(self, _m = 1., _b = 1.):
        self.m = float(_m)
        self.b = float(_b)

    def eval(self, x):
        return [self.m * x + self.b, x]

    def setParList(self, par):
        # only fit y intercept
        [self.b] = par

    def getParList(self):
        return [self.m, self.b]

    def guessFromData(self, x, y):
        l = int(0.07*len(x))
        y1 = numpy.average(y[-l:])
        y0 = numpy.average(y[:l])
        b = y1 - self.m * x[-1]
        return [b]

    # Output
    def __repr__(self):
        res = "\n#  m=%f\n#  b=%f"%(self.m, self.b)
        return res

#########################
if __name__ == '__main__':
    # simple demos
    pf = func(_m=-0.1, _b=0.5)
    pf.printPoints(10, 18.)
    print pf
