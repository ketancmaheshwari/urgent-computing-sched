#!/bin/bash

DATALOC=$1

#mkdir -p $DATALOC/csvdata
#
#TMPFILE=$(mktemp /tmp/XXXXX)
#
#for eachfile in $(find $DATALOC -iname '*.txt')
#do
#  tr ',' ';' < "$eachfile" > "$TMPFILE"
#  tr '|' ',' < "$TMPFILE" > "$DATALOC"/csvdata/"$eachfile".csv && rm "$TMPFILE"
#  awk -F, 'BEGIN{OFS=","}NF==60{print $0}' "$DATALOC"/csvdata/"$eachfile".csv > tmp && mv tmp "$DATALOC"/csvdata/"$eachfile".csv
#done

echo "$DATALOC/csvdata"
