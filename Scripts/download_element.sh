#!/bin/bash
inp=$1
_ele=${inp%%[0-9]*}
ele=${_ele,,}
Ele=${_ele^}
dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/neucbot-datasets/${ele}.git 
tar -xvzf ./${ele}/${Ele}.tar.gz
rm -rf ${ele}
cd $dir