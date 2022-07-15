#!/bin/bash

#
# This script downloads all elements for the JENDL dataset
#

dir=$PWD
cd ./Data/Isotopes/
git clone https://github.com/neucbot-datasets/jendl_data.git
tar -xvzf ./jendl_data/jendl_an_totalxs.tar.gz
rm -rf jendl_data
cd $dir
