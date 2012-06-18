#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
import sys
from FuncBase import FuncBase

class func(FuncBase):
	""" This is the pulse function and associated unilities for evaluating and fitting. """
	
	def __init__(self, _A=1., _alpha=1., _beta=1., toff=0.):
		self.A = float(_A)
		self.alpha = float(_alpha)
		self.beta = float(_beta)
		self.t0 = float(toff)

	def eval(self, x, baseline=None):
		if x - self.t0 < 0.0:
			if baseline is not None:
				return [baseline]
			else:
				return [0.0]
		# the pulse function
		v = self.A * (1.0 - math.exp(-(x-self.t0)*self.alpha)) * math.exp(-(x-self.t0)*self.beta)
		return [v, x - self.t0]

	# Utility functions for curve fitting

	def setParList(self, par):
		[self.A, self.alpha, self.beta, self.t0] = par

	def getParList(self):
		return [self.A, self.alpha, self.beta, self.t0]

	# Attributes of the fitted curve

	def getNormFactor(self):
		return self.alpha * self.A / (self.beta**2 + self.alpha * self.beta)

	def getAvgT(self):
		ta = (self.alpha + 2.* self.beta)/(self.beta*(self.alpha + self.beta))
		return ta + self.t0, self.eval(ta + self.t0)[0]

	def getPeakValue(self):
		return self.A*self.alpha*math.pow((1.+self.alpha/self.beta),(-1-self.beta/self.alpha))/self.beta
	
	def getPeakTime(self):
		peak = math.log(1. + (self.alpha/self.beta))/self.alpha
		return peak + self.t0, self.getPeakValue()

	def getInvFunc(self, v):
		tmpt, tmpP = self.getPeakTime()
		tg = 0
		# predjudice result for t > tpeak
		t = 2.*(tmpt - self.t0)
		eps = math.pow(10, (-7. + math.log10(t)))
		while abs(tg - t) > eps:
			tg = t
			t = self.tUpdater(tg, v)
			#print "<<<",tg,t,self.eval(t)[0],">>>"
		return t+self.t0,self.eval(t + self.t0)[0]

	def tUpdater(self, tg, v):
		num = self.A*(1. - math.exp(-self.alpha*tg))*math.exp(-self.beta*tg) - v
		denom = (self.alpha+self.beta)*math.exp(-(self.alpha+self.beta)*tg) - self.beta*math.exp(-self.beta*tg)
		return tg - num/(self.A*denom)

	def guessFromData(self, x, y):
		# find x at max y
		ymax = -99999999999
		for i in range(0,len(y)):
			if y[i] > ymax:
				ymax = y[i]
				xmax = x[i]
		xrange = (x[-1] - x[0])
		res = [ymax, 10./xrange, 1./xrange, xmax]
		return res

	# Output

	def __repr__(self):
		res = "\n#  A=%f\n#  alpha=%f\n#  beta=%f\n#  tOffset=%f\n"%tuple(self.getParList())
		res += "#  TPeak=%f,    FPeak=%f\n"%self.getPeakTime()
		res += "#  TAvgT=%f,    FAvg=%f\n"%self.getAvgT()
		res += "#  Norm=%f\n"%self.getNormFactor()
		res += "#  T1/2life=%f, F1/2Life=%f\n"%self.getInvFunc(self.getPeakValue()/2.)
		return res

#########################
if __name__ == '__main__':
	# simple demos
	pf = func(_A=30250, _alpha=690, _beta=30.5)
	pf.printPoints(0, .1)
	print pf
