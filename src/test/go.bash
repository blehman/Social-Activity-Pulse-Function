#!/usr/bin/env bash

if [ -e ./tmp ]; then
    rm ./tmp
    rm ./in.csv
    rm *.pdf
fi

for fun in doubleexp gamma lin exp gauss; do
    cat ../data/$fun.csv | ../fit.py -l $fun -f $fun >> ./tmp
done

cat ./tmp | grep -v "#" | grep -e "[0-9]" > in.csv
./plot.r
