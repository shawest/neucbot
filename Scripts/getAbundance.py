#!/usr/bin/python
import sys
import re

def findAbundance(iso):
    dir = "./Data/" #dir = "./Data/"
    fname = dir + "abundances.dat"
    f = open(fname)
    tokens = [re.split(" ", line) for line in f.readlines()]
    
    #find1 = "" #создаем пустую строку. ее не было 

    for words in tokens:
        for word in words:
            if word == iso:
            #[filter(None,words) for word if word == iso]
                #return isotopes += re.sub('[A-Z a-z]','',word) + " "
                #find1.append()
                #list([_f for _f in words if _f])
                #return words == words[2]
                #замена....
                return words[2]

def main(argv):
    iso = sys.argv[1] #iso = sys.argv[1]
    abundance = findAbundance(iso)
    print (abundance) #print abundance
    return abundance

if __name__ == '__main__' :
    main(sys.argv)

