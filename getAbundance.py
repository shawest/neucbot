#!/usr/bin/python
import sys
import re

def findAbundance(iso):
    dir = "./Data/"
    fname = dir + "abundances.dat"
    f = open(fname)
    tokens = [re.split(" ", line) for line in f.readlines()]

    for words in tokens:
        for word in words:
            if word == iso:
                return [_f for _f in words if _f][2]

def main(argv):
    iso = sys.argv[1]
    abundance = findAbundance(iso)
    print(abundance)
    return abundance

if __name__ == '__main__' :
    main(sys.argv)
            
