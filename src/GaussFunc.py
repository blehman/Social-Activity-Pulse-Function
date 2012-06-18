#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
import sys
from FuncBase import FuncBase

import scipy.special

class func(FuncBase):
	""" This is the gauss function and associated unilities for evaluating and fitting. """
	
	def __init__(self, _x0 = 0., _a = 1., _A0 = 1.):
		self.x0 = float(_x0)
		self.a = float(_a)
		self.A0 = float(_A0)

	def eval(self, x, baseline=None):
		arg = (x - self.x0)**2
		arg /= 2.*self.a**2
		return [self.A0 * math.exp(-arg)]

	def setParList(self, par):
		[self.x0, self.a, self.A0] = par

	def getParList(self):
		return [self.x0, self.a, self.A0]

	def guessFromData(self, x, y):
		ymax = -99999
		xymax = 0
		for i in range(0,len(y)):
			if y[i] > ymax:
				ymax = y[i]
				xymax = x[i]
		res = [xymax, (x[-1] - x[0])/10., ymax]
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
