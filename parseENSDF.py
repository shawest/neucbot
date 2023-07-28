#!/usr/bin/python
import sys
import os.path
import re
import getENSDFdata

intensityScale = 0
def getGammas(fname, energies, probs):
    f = open(fname)
    for line in f:
        if len(line) < 10:
            continue
        nucid = line[0:5]
        blank0 = line[5]
        if blank0 != ' ':
            continue
        comment = line[6]
        if comment != ' ':
            continue
        rad = line[7]
        if rad != 'G':
            continue
        blank1 = line[8]
        if blank1 != ' ':
            continue

        c = ''
        if len(line) > 77:
            c = line[77]
        if c == 'Q':
            continue

        ene = line[9:19]
        if ene == ' ':
            continue

        ene = float(ene)
        dEne = line[19:21]
        if not (dEne.isspace() or dEne == ''):
            dEne = float(dEne)
            
        prob = line[21:29]
        if (prob.isspace() or prob == ''):
            continue
        prob = float(prob)*intensityScale

        dri = line[29:31]
        if re.match("A-z", dri):
            dri = float(dri)
        
        energies.append(ene)
        probs.append(prob)

def getAlphas(fname, energies, probs):
    f = open(fname)
    for line in f:
        if len(line) < 10:
            continue
        nucid = line[0:5]
        blank0 = line[5]
        if blank0 != ' ':
            continue
        comment = line[6]
        if comment != ' ':
            continue
        rad = line[7]
        if rad != 'A':
            continue
        blank1 = line[8]
        if blank1 != ' ':
            continue

        c = ''
        if len(line) > 77:
            c = line[77]
        if c == 'Q':
            continue

        ene = line[9:19]
        if ene == ' ' or not ene[0].isdigit():
            continue

        ene = float(ene)
        dEne = line[19:21]
        if not (dEne.isspace() or dEne == '' or not dEne[0].isdigit()):
            dEne = float(dEne)
            
        prob = line[21:29]
        if (prob.isspace() or prob == ''):
            continue

        prob = float(prob)

        dri = line[29:31]
        if re.match("A-z", dri):
            dri = float(dri)
        
        energies.append(ene)
        probs.append(prob)

def getIntensityScale(fname):
    f = open(fname)
    for line in f:
        if len(line) < 10:
            continue
        nucid = line[0:5]
        blank0 = line[5]
        if blank0 != ' ':
            continue
        comment = line[6]
        if comment != ' ':
            continue
        rad = line[7]
        if rad != 'N':
            continue
            
        scale = line[9:19]
        if scale == '          ':
            intensityScale = 1
        else :
            intensityScale = float(scale)
        return intensityScale

def main(argv):
    if(len(argv) != 3):
        print('Usage: ./parseENSDF [element] [A]')
        return

    ele = argv[1]
    A = int(argv[2])
    indir = './Data/Decays/'
    finName = indir + 'ensdf' + ele.capitalize() + str(A) + '.dat'

    if(not os.path.isfile(finName)):
        getENSDFdata.main(argv)

    energies = []
    probs = []
    intensityScale = getIntensityScale(finName)
    getAlphas(finName,energies,probs)
    
    outdir = './AlphaLists/'
    foutName = outdir + ele.capitalize() + str(A) + 'Alphas.dat'
    fout = open(foutName,'w')

    for i in range(0,len(energies)):
#        print 'E =',energies[i]/1000,'\tI =',probs[i]
        fout.write(str(energies[i]/1000)+'\t'+str(probs[i])+'\n')
#        fout.write('{}\t{}\n'.format(energies[i]/1000, probs[i]))

if __name__ == "__main__":
    main(sys.argv)
