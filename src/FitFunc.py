#!/usr/bin/env python
#
#   Scott Hendrickson
#    2012-01-13
#
#########################

import math
import sys
from scipy import optimize

import PulseFunc

class FitFunc(object):
	def __init__(self, _data, _funcObj, _guess=None):
		self.f = _funcObj
		self.toVecs(_data)
		if _guess is None:
			self.initPars = self.f.guessFromData(self.x, self.y)
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
			res.append( [i] + self.f.eval(i) )
		return res

#########################
if __name__ == '__main__':
	# simple demos
	pf = PulseFunc.func(_A=30250, _alpha=690, _beta=30.5)
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
	fun = PulseFunc.func()
	fr = FitFunc(v, fun, p0)
	print fr.fit()
	# Use init param calculation algorithm
	fun1 = PulseFunc.func()
	fr = FitFunc(v, fun1)
	print fr.fit()

