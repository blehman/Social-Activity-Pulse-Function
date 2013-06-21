#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
import math
import numpy
from base_function import base_function

class func(base_function):
    """ This is the exponential function and associated utilities for evaluating and fitting. """
    def __init__(self, _a = 1., _A0 = 1.):
        self.a = float(_a)
        self.A0 = float(_A0)

    def eval(self, x):
        return [self.A0 * math.exp(self.a * x), x]

    def setParList(self, par):
        [self.a, self.A0] = par

    def getParList(self):
        return [self.a, self.A0]

    def guessFromData(self, x, y):
        y1 = numpy.log(y[-1])
        y0 = numpy.log(y[0])
        a = (y1 - y0)/(x[-1] - x[0])
        A = numpy.exp(numpy.log(y[0])/(a*x[0]))
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
