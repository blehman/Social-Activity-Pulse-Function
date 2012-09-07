#!/usr/bin/env bash
scp shendrickson@shendrickson4.gnip.com:/home/shendrickson/2012-08-29_bieberPlus2009/decomp/*.csv .
for x in *.csv; do
 ./decomp_plot.r $x $x
done

