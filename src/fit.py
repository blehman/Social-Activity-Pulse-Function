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

from FitPulseFunc import *

parser = OptionParser()
parser.add_option("-p", "--init-parameters", dest="init_parameters",
		                  help="Iinitial guess of parameters [A, alpha, beta, offset] ([] or blank ok)")
parser.add_option("-c", "--column",  dest="column", default=1,
				  help="Column for fit data (0 is independent var, default dependent is 1)")
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
fr = FitPulseFunc(d, p0)
print fr.fit()

print
wrt = csv.writer(sys.stdout)
for r1, r2 in zip(fr.eval(), d):
	wrt.writerow(r1+r2)
