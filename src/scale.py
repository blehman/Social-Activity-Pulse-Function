#!/usr/bin/env python
import sys
import csv
import fileinput

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-c", "--column",  dest="column_list", default="[2]",
    help="Columns to scale (append scaled column after column, default [2].")
parser.add_option("-t", "--time",  dest="time", default=False,action = "store_true",
    help="First column is independent variable start at zero (prepend new column).")
(options, args) = parser.parse_args()

exec("idx_list=[i-1 for i in %s]"%options.column_list)
extrema = [[sys.maxint, -sys.maxint] for i in idx_list]
wrt = csv.writer(sys.stdout)
data = []
for x in csv.reader(fileinput.FileInput(args,openhook=fileinput.hook_compressed)):
    try:
        tmp_list = [float(x[i]) for i in idx_list]
        if options.time:
            # this must be a number also
            tmp_indep = float(x[0])
        # if all numbers, then add to data set
        data.append(x)
        # get extrema
        for i in range(len(idx_list)):
            # order is min,max
            if tmp_list[i] < extrema[i][0]:
                extrema[i][0] = tmp_list[i]
            if tmp_list[i] > extrema[i][1]:
                extrema[i][1] = tmp_list[i]
    except ValueError:
        try:
            # maybe a header row?
            head = []
            for i in range(len(x)):
                head.append(x[i])
                if i in idx_list:
                    head.append("norm_%s"%x[i])
            if options.time:
                head.insert(0,"zero_%s"%x[0])
            wrt.writerow(head)
        except IndexError:
            wrt.writerow(x)
    except IndexError:
        wrt.writerow(x)

first = True
for x in data:
    if first:
        t0 = float(x[0][0])
        first = False
    tmp_out = []
    n_idx = 0
    for i in range(len(x)):
        tmp_out.append(x[i])
        if i in idx_list:
            tmp_out.append((float(x[i]) - extrema[n_idx][0])/(extrema[n_idx][1] - extrema[n_idx][0]))
            n_idx += 1
    if options.time:
        tmp_out.insert(0, float(x[0]) - t0)
    wrt.writerow(tmp_out)
