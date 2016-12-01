#!/bin/bash
_ele=$1
ele=${_ele,,}
Ele=${_ele^}
dir=$PWD
cd ./Data/Isotopes/
git clone git@github.com:neucbot-datasets/${ele}.git
tar -xvzf ./${ele}/${Ele}.tar.gz
rm -rf ${ele}
cd $dir