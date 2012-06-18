#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

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
parser.add_option("-r", "--range-list", dest="range_string", default = "[]",
		help="Function evaluation output range as '[start time, end time, number of points]' If not set, evaluate at fit points.")
(options, args) = parser.parse_args()

# p0 = [A, alpha, beta, t0]
if options.init_parameters is None or options.init_parameters == '[]':
	p0 = None
else:
	exec("p0=%s"%options.init_parameters)

# output range string
[tstart, tend, points] = [None, None, None]
if options.range_string <> '[]':
	exec('[tstart, tend, points] = %s'%options.range_string)

# read data
col = int(options.column)
d = []
for r in csv.reader(sys.stdin):
	try:
		d.append([float(r[0]), float(r[col])])
	except ValueError, e:
		print "Skipping text values (%s)"%','.join(r)

# fit type
if options.func_name == "lognorm":
	func = LogNormalCDFFunc.func()
elif options.func_name == "gauss":
	func = GaussFunc.func()
else:
	func = PulseFunc.func()
fr = FitFunc(d, func, p0)
# fit results
print fr.fit()

# blank line
print
wrt = csv.writer(sys.stdout)
# output is outer join of function and fit
d_dict = dict(d)
f_dict = dict(fr.eval(start=tstart, end=tend, points=points))

for time in sorted(list(set(d_dict.keys() + f_dict.keys()))):
	wrt.writerow([time, d_dict.get(time, None), time,  f_dict.get(time, None)])
