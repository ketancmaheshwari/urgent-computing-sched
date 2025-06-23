#!/bin/bash

DATALOC=$1
PARENTDIR=$(dirname "$DATALOC")
mkdir -p "$PARENTDIR"/csvdata

TMPFILE=$(mktemp /tmp/XXXXX)

for eachfile in $(find $DATALOC -iname '*.txt')
do
  fname=$(basename $eachfile)
  tr ',' ';' < "$eachfile" > "$TMPFILE"
  tr '|' ',' < "$TMPFILE" > "$PARENTDIR"/csvdata/"$fname".csv && rm "$TMPFILE"
  awk -F, 'BEGIN{OFS=","}NF==60{print $0}' "$PARENTDIR"/csvdata/"$fname".csv > "$TMPFILE" && mv "$TMPFILE" "$PARENTDIR"/csvdata/"$fname".csv
done

echo -n "$PARENTDIR/csvdata"
