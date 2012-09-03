#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
import sys
from base_function import base_function

import scipy.special

class func(base_function):
	""" This is the pulse function and associated unilities for evaluating and fitting. """
	
	def __init__(self, _s = 1., _m = 1.):
		self.S = float(_s)
		self.M = float(_m)

	def eval(self, x, baseline=None):
		arg = (math.log(x) - self.M)
		arg /= (math.sqrt(2.) * self.S)
		return [0.5*(1. + scipy.special.erf(arg))]

	def setParList(self, par):
		[self.S, self.M] = par

	def getParList(self):
		return [self.S, self.M]

	def guessFromData(self, x, y):
		res = [1., 1.]
		return res

	# Output
	
	def __repr__(self):
		res = "\n#  S=%f\n#  M=%f\n"%tuple(self.getParList())
		return res

#########################
if __name__ == '__main__':
	# simple demos
	pf = func(_s = 1., _m = 1.)
	pf.printPoints(0.1, 10.)
	print pf
