#!/usr/bin/env python
#
#   Scott Hendrickson
#    2011-11-03
#
#########################
import math
import sys
import csv
from optparse import OptionParser

from FitFunc import *
import PulseFunc
import LogNormalCDFFunc
import GaussFunc

parser = OptionParser()
parser.add_option("-p", "--init-parameters", dest="init_parameters",
		                  help="Iinitial guess of parameters [A, alpha, beta, offset] ([] or blank ok)")
parser.add_option("-c", "--column",  dest="column", default=1,
				  help="Column for fit data (0 is independent var, default dependent is 1)")
parser.add_option("-f", "--func-name",  dest="func_name", default="pulse",
				  help="pulse - Pulse Function (default); lognorm - log-normal CDF; gauss - gaussian PDF")
(options, args) = parser.parse_args()

# p0 = [A, alpha, beta, t0]
if options.init_parameters is None or options.init_parameters == '[]':
	p0 = None
else:
	exec("p0=%s"%options.init_parameters)

col = int(options.column)

d = []
for r in csv.reader(sys.stdin):
	try:
		d.append([float(r[0]), float(r[col])])
	except ValueError, e:
		print "Skipping text values (%s)"%','.join(r)

if options.func_name == "lognorm":
	func = LogNormalCDFFunc.func()
elif options.func_name == "gauss":
	func = GaussFunc.func()
else:
	func = PulseFunc.func()
fr = FitFunc(d, func, p0)
print fr.fit()

print
wrt = csv.writer(sys.stdout)
for r1, r2 in zip(fr.eval(), d):
	wrt.writerow(r1+r2)
