#!/usr/bin/env python
#
#   Scott Hendrickson
#    2011-11-03
#
#########################
import math
import sys

class func(object):
	""" This is the pulse function and associated unilities for evaluating and fitting. """
	
	def __init__(self, _A=1., _alpha=1., _beta=1., toff=0.):
		self.A = float(_A)
		self.alpha = float(_alpha)
		self.beta = float(_beta)
		self.t0 = float(toff)

	def eval(self, x, baseline=None):
		if x - self.t0 < 0.0:
			if baseline is not None:
				return baseline
			else:
				return 0.0
		# the pulse function
		v = self.A * (1.0 - math.exp(-(x-self.t0)*self.alpha)) * math.exp(-(x-self.t0)*self.beta)
		return v

        def evalVec(self, v):
		# Eval a vector of inputs
		return [self.eval(i) for i in v]

	# Utility functions for curve fitting

	def erf(self, par, x, y):
		# return the point-by-point delta
		res = []
		self.setParList(par)
		for i in range(0,len(y)):
			res.append(self.eval(x[i]) - y[i])
		return res
	
	def setParList(self, par):
		[self.A, self.alpha, self.beta, self.t0] = par

	def getParList(self):
		return [self.A, self.alpha, self.beta, self.t0]

	# Attributes of the fitted curve

	def getNormFactor(self):
		return self.alpha * self.A / (self.beta**2 + self.alpha * self.beta)

	def getAvgT(self):
		ta = (self.alpha + 2.* self.beta)/(self.beta*(self.alpha + self.beta))
		return ta + self.t0, self.eval(ta + self.t0)

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
			#print "<<<",tg,t,self.eval(t),">>>"
		return t+self.t0,self.eval(t + self.t0)

	def tUpdater(self, tg, v):
		num = self.A*(1. - math.exp(-self.alpha*tg))*math.exp(-self.beta*tg) - v
		denom = (self.alpha+self.beta)*math.exp(-(self.alpha+self.beta)*tg) - self.beta*math.exp(-self.beta*tg)
		return tg - num/(self.A*denom)

	# Output
	
	def printPoints(self, s, e, n=100):
		delta = (float(e) - float(s))/(n-1)
		for i in range(0,n):
			t = s + i*delta
			print "%s, %s"%(str(t), str(self.eval(t)))

	def __repr__(self):
		res = "\nA=%f\nalpha=%f\nbeta=%f\ntOffset=%f\n"%tuple(self.getParList())
		res += "TPeak=%f, FPeak=%f\n"%self.getPeakTime()
		res += "TAvgT=%f, FAvg=%f\n"%self.getAvgT()
		res += "Norm=%f\n"%self.getNormFactor()
		res += "T1/2life=%f, F1/2Life=%f\n"%self.getInvFunc(self.getPeakValue()/2.)
		return res

#############

from scipy import optimize

class FitPulseFunc(object):
	def __init__(self, _data, _guess=None):
		self.f = func()
		self.toVecs(_data)
		if _guess is None:
			self.initPars = self.guessFromData()
		else:
			self.initPars = _guess

	def toVecs(self, data):
		self.x = []
		self.y = []
		for d in data:
			self.x.append(d[0])
			self.y.append(d[1])
	
	def fit(self):
		self.fitPars, self.success = optimize.leastsq(self.f.erf, self.initPars, args=(self.x, self.y))
		self.f.setParList(self.fitPars)
		return self.f

	def eval(self):
		res = []
		for i in self.x:
			res.append([i, self.f.eval(i)])
		return res

	def guessFromData(self):
		# find x at max y
		ymax = -99999999999
		for i in range(0,len(self.y)):
			if self.y[i] > ymax:
				ymax = self.y[i]
				xmax = self.x[i]
		xrange = (self.x[-1] - self.x[0])
		res = [ymax, 10./xrange, 1./xrange, xmax]
		return res

#########################
if __name__ == '__main__':
	# simple demos
	pf = func(_A=30250, _alpha=690, _beta=30.5)
	pf.printPoints(0, .1)
	print pf

	p0 = [22000, 600, 10, .005]
	v = [	(0.0, 0.0),
		(0.0010101010101, 14722.0870054),
		(0.0020202020202, 21385.9328302),
		(0.0030303030303, 24171.3509832),
		(0.0040404040404, 25096.7012502),
		(0.0050505050505, 25136.414614),
		(0.0070707070707, 24196.4109866),
		(0.0090909090909, 22881.6344439),
		(0.0111111111111, 21544.8974262),
		(0.0121212121212, 20896.1721771),
		(0.0161616161616, 18477.4771294),
		(0.0171717171717, 17917.030074),
		(0.0222222222222, 15359.2544405),
		(0.0373737373737, 9675.50268403),
		(0.0424242424242, 8294.20261422),
		(0.0575757575758, 5224.89957942),
		(0.0626262626263, 4478.97924952),
		(0.0767676767677, 2909.79328641),
		(0.0808080808081, 2572.42676481),
		(0.0818181818182, 2494.38358616),
		(0.0929292929293, 1777.40200457),
		(0.0939393939394, 1723.47856384),
		(0.0989898989899, 1477.43025624)     ]
	print p0
	fr = FitPulseFunc(v, p0)
	print fr.fit()
	p1 = fr.guessFromData()
	print p1
	fr = FitPulseFunc(v, p0)
	print fr.fit()

