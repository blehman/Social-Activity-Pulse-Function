#!/usr/bin/env python
#
#   Scott Hendrickson
#    2011-11-03
#
#########################
import math
import sys

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
	
	def printPoints(self, s, e, n=100):
		delta = (float(e) - float(s))/(n-1)
		for i in range(0,n):
			t = s + i*delta
			dataTuple = tuple([str(t)] + [str(x) for x in self.eval(t)])
			fmtStr = "%s, "*(len(dataTuple)-1) + "%s"
			print fmtStr%dataTuple
