#!/bin/bash
inp=$1
_ele=${inp%%[0-9]*}
ele=`echo ${_ele} | tr '[:upper:]' '[:lower:]'`
ELE=`echo ${_ele} | tr '[:lower:]' '[:upper:]'`
Ele=${ELE:0:1}${ele:1:10}
dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/neucbot-datasets/${ele}.git 
tar -xvzf ./${ele}/${Ele}.tar.gz
rm -rf ${ele}
cd $dir