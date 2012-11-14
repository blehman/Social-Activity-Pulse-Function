#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
import math
from base_function import base_function
import scipy.special

class func(base_function):
    """ This is the gamma distribution function and associated unilities for evaluating and fitting. """
    def __init__(self, _x0 = 0., _a = 2., _b = 3., _A0 = 1.):
        self.x0 = float(_x0)
        self.a = float(_a)
        self.b= float(_b)
        self.A0 = float(_A0)

    def eval(self, x, baseline=None):
        arg = (x - self.x0) * self.A0
        if arg < 0:
            return [0.0]
        c = self.b**(-self.a)
        return [c * arg**(self.a - 1.) * math.exp(-arg/self.b)/scipy.special.gamma(self.a)]

    def setParList(self, par):
        [self.x0, self.a, self.b, self.A0] = par

    def getParList(self):
        return [self.x0, self.a, self.b, self.A0]

    def guessFromData(self, x, y):
        # find x at max y
        ymax = -99999999999
        for i in range(0,len(y)):
            if y[i] > ymax:
                ymax = y[i]
                xmax = x[i]
        xrng = (x[-1] - x[0])
        b = 0.5 * xrng 
        a =  (xmax/b) + 1
        A = 10./(ymax*xrng)
        x0 = x[0] 
        res = [x0, a, b, A]
        return res

    # Attributes of the fitted curve
    def getAvgT(self):
        ta = self.a * self.b
        return ta + self.x0, self.eval(ta + self.x0)[0]
    
    def getPeakTime(self):
        peak = self.b * (self.a - 1.)
        return peak + self.x0, self.eval(peak + self.x0)[0]

    def getHalfLife(self):
        #
        # Half the events have been observed
        #return t+self.x0,self.eval(t + self.x0)[0]
        return -1,-1

    # Output
    def __repr__(self):
        res =  "\n#  x0=%f\n#  a=%f\n#  b=%f\n#  A0=%f\n"%tuple(self.getParList())
        res += "#  tavg=%f   f(tavg)=%fi\n"%self.getAvgT()
        res += "#  tpeak=%f   f(tpeak)=%f\n"%self.getPeakTime()  
        #res += "#  t1/2life=%f   f(t1/2Life)=%f\n"%self.getHalfLife()
        return res

#########################
if __name__ == '__main__':
    # simple demos
    #pf = func(_x0 = 4, _a=1., _b=2., _A0=1)
    pf = func(_x0 = 4, _a=3., _b=1., _A0=1)
    pf.printPoints(0, 12.)
    print pf
