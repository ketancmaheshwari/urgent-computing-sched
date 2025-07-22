#!/bin/bash

HTMLFILE=$1
PNGFILE=$2

echo '****'
echo $PWD
echo $HTMLFILE
echo $PNGFILE
echo '****'

firefox --no-remote --profile /tmp --screenshot $PWD/$PNGFILE "file://$PWD/$HTMLFILE"

