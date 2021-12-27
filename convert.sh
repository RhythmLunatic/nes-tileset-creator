#!/bin/bash
rm -r out
mkdir out
./tileExport.py "$1"
cd out
montage $(ls | sort -V | xargs) -geometry 16x16 ../output.png
cd ..
