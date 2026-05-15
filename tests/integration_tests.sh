#!/bin/bash

###################
# Th232 ChainList #
###################

echo
echo "Running test..."
echo "---------------------"
echo "Materials/Acrylic.dat"
echo "Chains/Th232Chain.dat"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -c Chains/Th232Chain.dat -o tmp-acrylic-th232-chain.txt
diff tmp-acrylic-th232-chain.txt tests/integration_tests/acrylic-th232-chain.txt

# If the previous diff command generated any differences, the exit code will be 1
# and this will be considered a test failure.
if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-th232-chain.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-th232-chain.txt
fi

##################
# U235 ChainList #
##################

echo
echo "Running test..."
echo "---------------------"
echo "Materials/Acrylic.dat"
echo "Chains/U235Chain.dat"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -c Chains/U235Chain.dat -o tmp-acrylic-u235-chain.txt
diff tmp-acrylic-u235-chain.txt tests/integration_tests/acrylic-u235-chain.txt

# If the previous diff command generated any differences, the exit code will be 1
# and this will be considered a test failure.
if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-u235-chain.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-u235-chain.txt
fi

##################
# U238 ChainList #
##################

echo
echo "Running test..."
echo "---------------------"
echo "Materials/Acrylic.dat"
echo "Chains/U238Chain.dat"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -c Chains/U238lowerChain.dat -o tmp-acrylic-u238-chain.txt
diff tmp-acrylic-u238-chain.txt tests/integration_tests/acrylic-u238-chain.txt

# If the previous diff command generated any differences, the exit code will be 1
# and this will be considered a test failure.
if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-u238-chain.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-u238-chain.txt
fi

###################
# Rn220 AlphaList #
###################

echo
echo "Running test..."
echo "---------------------"
echo "Materials/Acrylic.dat"
echo "AlphaLists/Rn220Alphas.dat"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -l AlphaLists/Rn220Alphas.dat -o tmp-acrylic-rn220-alphalist.txt
diff tmp-acrylic-rn220-alphalist.txt tests/integration_tests/acrylic-rn220-alphalist.txt

if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-rn220-alphalist.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-rn220-alphalist.txt
fi

###################
# Bi212 AlphaList #
###################

echo
echo "Running test..."
echo "---------------------"
echo "Materials/Acrylic.dat"
echo "AlphaLists/Bi212Alphas.dat"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -l AlphaLists/Bi212Alphas.dat -o tmp-acrylic-bi212-alphalist.txt
diff tmp-acrylic-bi212-alphalist.txt tests/integration_tests/acrylic-bi212-alphalist.txt

if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-bi212-alphalist.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-bi212-alphalist.txt
fi

##############################
# Bi212 AlphaList - Raw Data #
##############################

echo
echo "Running test with raw data..."
echo "-----------------------------"
echo "Materials/Acrylic.dat"
echo "AlphaLists/Bi212Alphas.dat"
echo "DATA SOURCE: talys-raw"
echo

python3 ./neucbot.py -m Materials/Acrylic.dat -l AlphaLists/Bi212Alphas.dat -d v2 -o tmp-acrylic-bi212-alphalist.txt --data-source talys-raw
diff tmp-acrylic-bi212-alphalist.txt tests/integration_tests/acrylic-bi212-alphalist.txt

if [ $? -eq 1 ]; then
  echo
  echo "Test failed" >&2
  echo
  rm tmp-acrylic-bi212-alphalist.txt

  exit 1
else
  echo
  echo "Test passed"
  echo
  rm tmp-acrylic-bi212-alphalist.txt
fi

############################
# TALYS Recalculation Test #
############################

# echo
# echo "Running test with TALYS..."
# echo "--------------------------"
# echo "Materials/Acrylic.dat"
# echo "AlphaLists/Bi212Alphas.dat"
# echo "DATA SOURCE: talys-raw"
# echo

# echo "Removing subset of TALYS files..."
# rm Data/Isotopes/C/C12/TalysOut/outputE0.0*
# rm Data/Isotopes/C/C12/NSpectra/nspec000.0*

# echo "Running neucbot.py with -t enabled..."
# python3 ./neucbot.py -m Materials/Acrylic.dat -l AlphaLists/Bi212Alphas.dat -d v2  -t --data-source talys-raw

# # Since ./neucbot.py prints TALYS information when it is enabled, the output file won't be exactly the same.
# # The run above downloads the missing files from TALYS and this subsequent run
# # verifies the output.
# echo "Running neucbot.py to verify successful TALYS download..."
# python3 ./neucbot.py -m Materials/Acrylic.dat -l AlphaLists/Bi212Alphas.dat -d v2 -o tmp-acrylic-bi212-alphalist.txt --data-source talys-raw
# diff tmp-acrylic-bi212-alphalist.txt tests/integration_tests/acrylic-bi212-alphalist.txt

# if [ $? -eq 1 ]; then
#   echo
#   echo "Test failed" >&2
#   echo
#   rm tmp-acrylic-bi212-alphalist.txt

#   exit 1
# else
#   echo
#   echo "Test passed"
#   echo
#   rm tmp-acrylic-bi212-alphalist.txt
# fi


echo "All tests passed, no regressions introduced."

