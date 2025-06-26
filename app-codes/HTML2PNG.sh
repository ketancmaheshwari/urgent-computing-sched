#!/bin/bash

HTMLFILE=$1
PNGFILE=$2

echo '****'
echo $PWD
echo $HTMLFILE
echo $PNGFILE
echo '****'

killall firefox
sleep 1
/usr/bin/firefox --screenshot $PWD/$PNGFILE "file://"$PWD/$HTMLFILE

