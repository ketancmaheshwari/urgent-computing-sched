#!/bin/bash

HTMLFILE=$1
PNGFILE=$2

/usr/bin/firefox --screenshot $PNGFILE "file://"$HTMLFILE

