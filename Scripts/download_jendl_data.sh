#!/bin/bash

#
# This script downloads all elements for the JENDL dataset
#

dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/iv-gonch/jendl_data
tar -xvzf ./jendl_data/B.tar.gz
tar -xvzf ./jendl_data/Be.tar.gz
tar -xvzf ./jendl_data/C.tar.gz
tar -xvzf ./jendl_data/F.tar.bz2
tar -xvzf ./jendl_data/Li.tar.gz
tar -xvzf ./jendl_data/N.tar.gz
tar -xvzf ./jendl_data/Na.tar.bz2
tar -xvzf ./jendl_data/O.tar.bz2
rm -rf jendl_data
cd $dir
