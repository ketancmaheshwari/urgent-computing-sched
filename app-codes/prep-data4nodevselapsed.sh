#!/bin/bash

INDATAFILE=$1

awk -F, 'BEGIN{OFS=","; print "Elapsedmins, Nodes"}{n=int($20/60); if(n>0) {print n,$36}}' $INDATAFILE

