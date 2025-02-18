#!/bin/bash

#
# This script downloads elements for the V2 dataset, generated with TALYS-1.95
#
# Usage: ./download_element.sh <element>

inp=$1
_ele=${inp%%[0-9]*}
ele=`echo ${_ele} | tr '[:upper:]' '[:lower:]'`
ELE=`echo ${_ele} | tr '[:lower:]' '[:upper:]'`
Ele=${ELE:0:1}${ele:1:10}
dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/neucbot-datasets/${ele}_v2.git 
tar -xvzf ./${ele}_v2/${Ele}.tar.gz
rm -rf ${ele}_v2
cd $dir