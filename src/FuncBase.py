#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
import sys
import numpy

class FuncBase(object):
	
        def evalVec(self, v):
		# Eval a vector of inputs
		return [self.eval(i)[0] for i in v]

	def erf(self, par, x, y):
		# return the point-by-point delta
		res = []
		self.setParList(par)
		for i in range(0,len(y)):
			res.append(self.eval(x[i])[0] - y[i])
		return res
	
	def evalPoints(self, t):
		for i,j in zip(t, self.evalVec(t)):
			yield [i,j]

	def printPoints(self, s, e, n=100):
		# convenience printing function
		for dataTuple in self.evalPoints(numpy.linspace(s,e,n)):
			fmtStr = "%s, "*(len(dataTuple)-1) + "%s"
			print fmtStr%tuple(dataTuple)
