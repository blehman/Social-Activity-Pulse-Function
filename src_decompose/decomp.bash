#!/usr/bin/env bash
base=/home/shendrickson
working=2012-08-29_bieberPlus2009
tsutil="$base/Social-Activity-Pulse-Function/src_decompose/timeseries.py -c2"
ddir=$base/$working/decomp
if [ ! -d $ddir ]; then
 mkdir $ddir
fi

#export PYTHONPATH=${PYTHONPATH}:$base/Social-Activity-Pulse-Function/src_decompose/:$base/Social-Activity-Pulse-Function/src/
#echo $PYTHONPATH
cd $base/$working/rdata
for fl in *.byhour.csv ; do
 echo "Decomposing $fl..."
 cat $fl | $tsutil > $ddir/$fl.decom.csv
done
