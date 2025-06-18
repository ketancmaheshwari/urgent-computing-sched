#!/bin/bash

DATALOC=$1

TMPFILE=$(mktemp /tmp/XXXXX)

for eachfile in $(find $DATALOC -iname '*.txt')
do
if grep ';' "$eachfile"
then
  echo "Data contains semi-colons, new replacement character needed."
  exit 1
else
  tr ',' ';' < "$eachfile" > "$TMPFILE"
  tr '|' ',' < "$TMPFILE" > "$DATALOC"/"$eachfile".csv && rm "$TMPFILE"
fi
done

