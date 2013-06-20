#!/usr/bin/env bash

if [ -e ./tmp ]; then
    rm ./tmp
fi

for fun in doubleexp gamma lin exp gauss; do
    cat ../data/$fun.csv | ../fit.py -f $fun >> ./tmp
done

