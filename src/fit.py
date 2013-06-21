#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import math
import sys
import csv
import fileinput
from optparse import OptionParser

from function_fit import *
import doubleexp_function
import lognormal_function
import gauss_function
import exp_function
import gamma_function
import lin_function

parser = OptionParser()
parser.add_option("-p", "--init-parameters", dest="init_parameters",
        help="Iinitial guess of parameters [A, alpha, beta, offset] ([] or blank ok)")
parser.add_option("-i", "--column-independent", dest="icolumn", default=1,
        help="column of independent variable to fit (default is 1)")
parser.add_option("-c", "--column-dependent",  dest="column", default=2,
        help="Column of dependent variable to fit (default is 2)")
parser.add_option("-l", "--append-label",  dest="label", default=None,
        help="Append label column (useful as R factor)")
parser.add_option("-f", "--func-name",  dest="func_name", default="dubex",
        help="gamma - gamma distribution; exp - exponential; dubex - Pulse Function (default); lognorm - log-normal CDF; gauss - gaussian PDF")
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
col = int(options.column) - 1
icol = int(options.icolumn) - 1
# keep leading columns for output
lead_cols = {}
d = []
for r in csv.reader(fileinput.FileInput(args,openhook=fileinput.hook_compressed)):
    try:
        tmp = float(r[icol])
        d.append([tmp, float(r[col])])
        lead_cols[tmp] = r[:icol]
        padding = ["n/a" for x in lead_cols[tmp]]
    except ValueError, e:
        print "Skipping text values (%s)"%','.join(r)

# fit type
if options.func_name == "lognorm":
    func = lognormal_function.func()
elif options.func_name == "gauss":
    func = gauss_function.func()
elif options.func_name == "exp":
    func = exp_function.func()
elif options.func_name == "gamma":
    func = gamma_function.func()
elif options.func_name == "lin":
    func = lin_function.func()
else:
    func = doubleexp_function.func()
fr = function_fit(d, func, p0)

# fit results
print fr.fit()

# blank line
print
wrt = csv.writer(sys.stdout)
# output is outer join of function and fit
d_dict = dict(d)
f_dict = dict(fr.eval(start=tstart, end=tend, points=points))

for time in sorted(list(set(d_dict.keys() + f_dict.keys()))):
    res = lead_cols.get(time, padding) + [time, d_dict.get(time, "n/a"), time,  f_dict.get(time, "n/a")]
    if options.label:
        res.append(options.label)
    wrt.writerow(res)
