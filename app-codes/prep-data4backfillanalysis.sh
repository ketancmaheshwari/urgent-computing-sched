#!/bin/bash

INDATAFILE=$1

awk -F, 'BEGIN{OFS=","; print "Diffsec,Nodes,State,Backfilled"}{diff=($7*60)-$20; if(index($57,"SchedBackfill")!=0){backfill="yes"}else{backfill="no"} print diff, $36, $11, backfill}' $INDATAFILE

