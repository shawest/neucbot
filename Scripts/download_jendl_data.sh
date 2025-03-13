#!/bin/bash

#
# This script downloads elements from the JENDL-5 dataset
#
# Usage: bash ./Scripts/download_lendl_data.sh <element>

inp=$1
_ele=${inp%%[0-9]*}
ele=`echo ${_ele} | tr '[:upper:]' '[:lower:]'`
ELE=`echo ${_ele} | tr '[:lower:]' '[:upper:]'`
Ele=${ELE:0:1}${ele:1:10}
dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/neucbot-datasets/${Ele}_JENDL-5.git 

if [[ "$Ele" == "O" || "$Ele" == "F" || "$Ele" == "Na" ]]; then
    tar -xvjf ./${Ele}_JENDL-5/${Ele}.tar.bz2
else
    tar -xvzf ./${Ele}_JENDL-5/${Ele}.tar.gz
fi

rm -rf ${Ele}_JENDL-5
cd $dir

# List of JENDL elemets:
# bash Scripts/download_jendl_data.sh Li
# bash Scripts/download_jendl_data.sh Be
# bash Scripts/download_jendl_data.sh B 
# bash Scripts/download_jendl_data.sh C 
# bash Scripts/download_jendl_data.sh N 
# bash Scripts/download_jendl_data.sh O 
# bash Scripts/download_jendl_data.sh F 
# bash Scripts/download_jendl_data.sh Na