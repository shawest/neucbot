#!/usr/bin/python
import sys
import re

def findIsotopes(ele):
    dir = "./Data/"
    fname = dir + "abundances.dat"
    f = open(fname)
    tokens = map(lambda line: re.split(" ", line), f.readlines())
    
    isotopes = ""

    for words in tokens:
        for word in words:
            if re.sub('[0-9]','',word) == ele.capitalize():
                isotopes += re.sub('[A-Z a-z]','',word) + " "

    return isotopes

def main(argv):
    ele = argv[1]
    print findIsotopes(ele)

if __name__ == '__main__':
    main(sys.argv)
