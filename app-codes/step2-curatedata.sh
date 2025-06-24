#!/bin/bash

eachfile=$1
TMPFILE=$(mktemp /tmp/XXXXX)

tr ',' ';' < "$eachfile" | tr '|' ',' | sed 's/CANCELLED by [0-9].*/CANCELLED/g' | awk -F, 'BEGIN{OFS=","}NF==60{if($1){print $0}}'

