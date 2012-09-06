#!/usr/bin/env python
__author__="Scott Hendrickson"
__email__="shendrickson@gnip.com"
__license__="http://creativecommons.org/licenses/by-sa/3.0/"
###

import numpy
import sys
import csv
from optparse import OptionParser
import datetime
import re
import time
import timeseries_decompose

parser = OptionParser()
parser.add_option("-c", "--column",  dest="column", default=1,
        help="Column for decompose data (date string in any column, default decompose is 1)")
parser.add_option("-a", "--alt-date-1", action="store_true", dest="alt_date_1", default=False,
        help="alt-date-1: %d %b %Y %H:%M:%S (default: %Y-%m-%d %H:%M:%S)")
parser.add_option("-e", "--alt-date-2", action="store_true", dest="alt_date_2", default=False,
        help="alt-date-2: %b %d %H:%M:%S UTC %Y (default: %Y-%m-%d %H:%M:%S)")
(options, args) = parser.parse_args()

if options.alt_date_1:
        #Example Mon, 24 Oct 2011 08:29:07 GMT   (skip the dow)
        timeRE = re.compile("[0-9]{2} [a-zA-Z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}")
        fmtStr = "%d %b %Y %H:%M:%S"
elif options.alt_date_2:
        #Example May 31 19:18:20 UTC 2012   (skip the dow)
        timeRE = re.compile("[a-zA-Z]{3} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} UTC [0-9]{4}")
        fmtStr = "%b %d %H:%M:%S U C %Y"
else:
        #twitter and facebook
        timeRE = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2}.[0-9]{2}:[0-9]{2}:[0-9]{2}")
        fmtStr = "%Y-%m-%d %H:%M:%S"

# read data
col = int(options.column)
data = []
last = None
last_delta = None
for r in csv.reader(sys.stdin):
    try:
        rowTime = timeRE.search(' '.join(r)).group(0).replace("T"," ")
    except AttributeError, e:
        print >>sys.stderr, str(e), str(r)
        sys.exit()
    sampleDatetime = datetime.datetime.strptime(rowTime, fmtStr)
    try:
        # first column is datetime string
        tmp = [str(sampleDatetime), time.mktime(sampleDatetime.utctimetuple()), float(r[col])]
        data.append(tmp)
        if last is not None:
            if last_delta != sampleDatetime - last:
                sys.stderr.write("Data interval inconsistent (%s)\n")
            last_delta = sampleDatetime - last
            last = sampleDateTime
    except ValueError, e:
        print "Skipping text values (%s)"%','.join(r)

tss = timeseries_decompose.timeseries_decompose(data)
tss.csv()
