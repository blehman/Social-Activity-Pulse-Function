#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
from base_function import base_function

class func(base_function):
    """ This is the exponential function and associated unilities for evaluating and fitting. """
    
    def __init__(self, _x0 = 0., _a = 1., _A0 = 1.):
        self.x0 = float(_x0)
        self.a = float(_a)
        self.A0 = float(_A0)

    def eval(self, x, baseline=None):
        arg = (x - self.x0)
        return [self.A0 * math.exp(self.a * arg)]

    def setParList(self, par):
        [self.x0, self.a, self.A0] = par

    def getParList(self):
        return [self.x0, self.a, self.A0]

    def guessFromData(self, x, y):
        a = (math.log(y[-1]) - math.log(y[0]))/(x[-1] - x[0])
        A = y[0]
        x0 = x[0] 
        res = [x0, a, A]
        return res

    # Output
    
    def __repr__(self):
        res = "\n#  x0=%f\n#  a=%f\n#  A0=%f"%tuple(self.getParList())
        return res

#########################
if __name__ == '__main__':
    # simple demos
    pf = func(_x0 = 4, _a=2., _A0=1)
    pf.printPoints(0, 8.)
    print pf
