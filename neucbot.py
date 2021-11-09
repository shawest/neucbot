#!/usr/bin/python
from __future__ import print_function
import sys
import os
sys.path.insert(0, './Scripts/')
import re
import subprocess
import shutil
import math
import parseENSDF as ensdf
import getNaturalIsotopes as gni
import getAbundance as isoabund

class constants:
    N_A = 6.0221409e+23
    MeV_to_keV= 1.e3
    mb_to_cm2 = 1.e-27
    year_to_s = 31536000 
    min_bin   = 0   # keV
    max_bin   = 20000  # keV
    delta_bin = 100 # keV
    run_talys  = False
    run_alphas = True
    print_alphas = False
    download_data = False
    download_version = 2
    force_recalculation = False
    ofile = sys.stdout

class material:
    def __init__(self,e,a,f):
        self.ele = str(e)
        self.A = float(a)
        self.frac = float(f)

def isoDir(ele,A):
    return './Data/Isotopes/'+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'

def parseIsotope(iso):
    ele = ''
    A = 0
    for i in iso:
        if i.isalpha():
            ele += i
        if i.isdigit():
            A = A*10 + int(i)
    return [ele,A]

def generateAlphaFileName(ele,A):
    outdir = './AlphaLists/'
    fName = outdir + ele.capitalize() + str(A) + 'Alphas.dat'
    return fName

def generateAlphaList(ele, A):
    print('generateAlphaList(',ele,A,')',file=constants.ofile)
    ensdf.main(['parseENSDF',ele,A])

def loadAlphaList(fname):
    f = open(fname)
    tokens = map(lambda line: line.split(), f.readlines())
    alpha_list = []
    for words in tokens:
        if words[0][0] == '#' or len(words) < 2:
            continue

        alpha = []
        for word in words:
            alpha.append(float(word))
        alpha_list.append(alpha)
    f.close()
    return alpha_list

def getAlphaList(ele,A):
    fname = generateAlphaFileName(ele,A)
    return loadAlphaList(fname)

def getAlphaListIfExists(ele,A):
    fName = generateAlphaFileName(ele,A)
    tries = 3
    while not os.path.isfile(fName):
        if tries < 0:
            print('Cannot generate alpha list for ele = ', ele,  ' and A = ', A,file = constants.ofile)
            return 0
        print('generating alpha file ', fName, file = constants.ofile)
        generateAlphaList(ele,A)
        tries -= 1
    return getAlphaList(ele,A)

def loadChainAlphaList(fname):
    f = open(fname)
    tokens = map(lambda line: line.split(), f.readlines())
    alpha_list = []
    for line in tokens:
        if len(line) < 2 or line[0][0] == '#':
            continue
        # Read isotope and its branching ratio from file
        iso = line[0]
        br = float(line[1])
        [ele,A] = parseIsotope(iso)
        
        # Now get the isotope's alpha list and add it to the chain's list
        aList_forIso = getAlphaListIfExists(ele,A)
        if constants.print_alphas:
            print(iso, file = constants.ofile)
            print('\t', aList_forIso, file = constants.ofile)
        for [ene,intensity] in aList_forIso:
            alpha_list.append([ene, intensity*br/100])
    return alpha_list

def readTargetMaterial(fname):
    f = open(fname)
    mat_comp = []
    tokens = map(lambda line: line.split(), f.readlines())
    for line in tokens:
        if len(line) < 3:
            continue
        if line[0][0] == '#':
            continue
        ele = line[0].lower()
        A = int(line[1])
        frac = float(line[2])

        if A == 0:
            natIso_list = gni.findIsotopes(ele).split()
            for A_i in natIso_list:
                abund = float(isoabund.findAbundance(str(A_i)+ele.capitalize()))
                mater = material(ele,A_i,frac*abund/100.)
                mat_comp.append(mater)
        else:
            mater = material(ele,A,frac)
            mat_comp.append(mater)

    # Normalize
    norm = 0
    for mat in mat_comp:
        norm += mat.frac
    for mat in mat_comp:
        mat.frac /= norm

    return mat_comp

def calcStoppingPower(e_alpha_MeV,mat_comp):
    # Stopping power as units of keV/(mg/cm^2) or MeV/(g/cm^2)
    e_alpha = e_alpha_MeV
    sp_total = 0
    # First, reduce the material to combine all isotopes with the same Z
    mat_comp_reduced = {}
    for mat in mat_comp:
        if mat.ele in mat_comp_reduced:
            mat_comp_reduced[mat.ele] += mat.frac
        else:
            mat_comp_reduced[mat.ele] = mat.frac
    
    # Then, for each element, get the stopping power at this alpha energy
    for mat in mat_comp_reduced:
        spDir = './Data/StoppingPowers/'
        spFile = spDir + mat.lower() + '.dat'
        spf = open(spFile)
        
        tokens = map(lambda line: line.split(), spf.readlines())
        first = True
        sp_found = False
        e_curr = 0
        e_last = 0
        sp_curr = 0
        sp_last = 0
        sp_alpha = 0
        for line in tokens:
            if line[0][0] == '#':
                continue
            e_curr = float(line[0])
            if str(line[1]) == 'keV':
                e_curr /= 1000
            elif str(line[1]) == 'MeV':
                e_curr *= 1
            sp_curr = float(line[3])+float(line[2])
            
            # Alpha energy is below the list. Use the lowest energy in the list
            if e_curr > e_alpha and first:
                first = False
                sp_found = True
                sp_alpha = sp_curr
                break
            # If this entry is above the alpha energy, the alpha is between this
            # entry and the previous one
            if e_curr > e_alpha:
                first = False
                sp_alpha = (sp_curr-sp_last)*(e_alpha-e_last)/(e_curr-e_last) + sp_last
                sp_found = True
                break
            # Otherwise, keep looking for the entry
            first = False
            sp_last = sp_curr
            e_last = e_curr
        # if the alpha energy is too high for the list, use the highest energy on the list
        if not sp_found:
            sp_alpha = sp_last
        sp_total += sp_alpha * mat_comp_reduced[mat]/100
    return sp_total

def runTALYS(e_a, ele, A):
    iso = str(ele)+str(int(A))
    inpdir = isoDir(ele,A) + 'TalysInputs/'
    outdir = isoDir(ele,A) + 'TalysOut/'
    nspecdir= isoDir(ele,A) + 'NSpectra/'
    if not os.path.exists(inpdir):
        os.makedirs(inpdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(nspecdir):
        os.makedirs(nspecdir)

#    command = "\nprojectile a\nejectiles p n g\nelement "+ele+"\nmass "+str(int(A))+"\nenergy "+str(e_a)+"\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2\n"
    command = "\nprojectile a\nejectiles p n g\nelement "+ele+"\nmass "+str(int(A))+"\nenergy "+str(e_a)+"\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2"

    inp_fname = inpdir+"inputE"+str(e_a)
    inp_f = open(inp_fname,'w')
    inp_f.write(command)
    inp_f.close()
    out_fname = outdir+"outputE"+str(e_a)
    
    bashcmd = 'talys < '+inp_fname+' > '+out_fname
    print('Running TALYS:\t ', bashcmd, file = constants.ofile)
    runscript_fname = "./runscript_temp.sh"
    runscript_f = open(runscript_fname,"w")
    runscript_f.write("#!/usr/bin/bash\n\n"+bashcmd)
    runscript_f.close()
    process = subprocess.call(bashcmd,shell=True)
    # Move the output neutron spectrum to the appropriate directory
    ls = os.listdir("./")

    moved_file = False
    for f in ls:
        if "nspec" in f:
            if os.path.exists(nspecdir+f):
                os.remove(nspecdir+f)
            fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
            shutil.move(f, fname)
            moved_file = True
    # If no neutron spectrum file is found, make a blank one
    if not moved_file:
        fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
        blank_f = open(fname,'w')
        blank_f.write("EMPTY")
        blank_f.close()
        

def getMatTerm(mat,mat_comp):
    # mat_comp structure: [ele,A,frac]
    A = mat.A
    conc = mat.frac/100.
    mat_term = (constants.N_A * conc)/A
    return mat_term

def getIsotopeDifferentialNSpec(e_a, ele, A):
    target = ele+str(int(A))
    path = isoDir(ele,A) + 'NSpectra/'
    if not os.path.exists(path):
        os.makedirs(path)
    fname = path+'nspec{0:0>7.3f}.tot'.format(int(100*e_a)/100.)
    outpath = isoDir(ele,A) + 'TalysOut'
    if constants.force_recalculation:
        print('Forcibily running TALYS for', int(100*e_a)/100., 'alpha on', target, file = constants.ofile)
        print('Outpath', outpath, file = constants.ofile)
        runTALYS(int(100*e_a)/100.,ele,A)
           
    # If the file does not exist, run TALYS
    if not os.path.exists(fname):
        if constants.run_talys:
            while not os.path.exists(fname):
                print('Running TALYS for', int(100*e_a)/100., 'alpha on', target, file = constants.ofile)
                print('Outpath', outpath, file = constants.ofile)
                runTALYS(int(100*e_a)/100.,ele,A)
                ls = os.listdir(outpath)
        else:
            print("Warning, no (alpha,n) data found for E_a =", e_a,"MeV on target", target,"...skipping. Consider running with the -d or -t options", file = constants.ofile)
            return {}
    
    # Load the file
    # If no output was produced, skip this energy
    if not os.path.exists(outpath):
        return {}

    f = open(fname)
    spec = {}
    tokens = map(lambda line: line.split(), f.readlines())
    for line in tokens:
        if len(line) < 1 or line[0] == 'EMPTY':
            break
        if line[0][0] == '#':
            continue
        # line[0] = E-out
        # line[1] = Total
        # line[2] = Direct
        # line[3] = Pre-equil
        # line[4] = Mult. preeq
        # line[5] = Compound
        # line[6] = Pre-eq ratio
        # convert from mb/MeV to cm^2/MeV
        energy = int(float(line[0])*constants.MeV_to_keV)
        sigma = float(line[1])*constants.mb_to_cm2/constants.MeV_to_keV
        spec[energy] = sigma
    return spec
    
def rebin(histo,step,minbin,maxbin):
    nbins = (maxbin-minbin)/step
    newhisto = {}
    normhisto = {}
    for i in sorted(histo):
        index = sorted(histo).index(i)
        # Get the spacing between points
        delta = sorted(histo)[0]
        if index > 0:
            delta = sorted(histo)[index] - sorted(histo)[index-1]
        # If the x value is too low, put it in the underflow bin (-1)
        if i < minbin:
            print('Underflow: ', i, ' (minbin = ', minbin, ')',file = constants.ofile)
            if -1 in newhisto:
                newhisto[-1] += histo[i]*delta
                normhisto[-1] += delta
            else:
                newhisto[-1] = histo[i]*delta
                normhisto[-1] = delta
        # ...or the overflow bin if too high
        if i > maxbin:
            print('Overflow: ', histo[i], ' (maxbin = ', maxbin,')', file = constants.ofile)
            overflowbin = int(nbins+10*step)
            if overflowbin in newhisto:
                newhisto[overflowbin] += histo[i]*delta
                normhisto[overflowbin] += delta
            else:
                newhisto[overflowbin] = histo[i]*delta
                normhisto[overflowbin] = delta
        # Otherwise, calculate the bin
        newbin = int(minbin+int((i-minbin)/step)*step)
        if newbin in newhisto:
            newhisto[newbin] += histo[i]*delta
            normhisto[newbin] += delta
        else:
            newhisto[newbin] = histo[i]*delta
            normhisto[newbin] = delta

    # Renormalize the new histogram
    for i in newhisto:
        if normhisto[i] > 0:
            newhisto[i] /= normhisto[i]

    return newhisto

def integrate(histo):
    integral = 0
    for i in sorted(histo):
        # Get the bin width
        delta = sorted(histo)[0]
        index = sorted(histo).index(i)
        if index > 0:
            delta = sorted(histo)[index] - sorted(histo)[index-1]

        integral += histo[i]*delta
    return integral
    
def readTotalNXsect(e_a,ele,A):
    fname = isoDir(ele,A) + 'TalysOut/outputE' + str(int(100*e_a)/100.)
    if not os.path.exists(fname):
        print("Could not find file ", fname, file = constants.ofile)
        return 0
    f = open(fname)
    lines = map(lambda line: line.split(), f.readlines())
    xsect_line  = 0
    for line in lines:
        if line == ['2.','Binary','non-elastic','cross','sections','(non-exclusive)']:
            break
        else:
            xsect_line += 1
    
    xsect_line += 3
    if len(lines) < xsect_line:
        return 0
    if lines[xsect_line][0] != 'neutron':
        return 0
    sigma = float(lines[xsect_line][2])
    sigma *= constants.mb_to_cm2
    return sigma

def condense_alpha_list(alpha_list,alpha_step_size):
    alpha_ene_cdf = []
    max_alpha = max(alpha_list)
    e_a_max = int(max_alpha[0]*100 + 0.5)/100.
    alpha_ene_cdf.append([e_a_max,max_alpha[1]])
    e_a = e_a_max
    while e_a > 0:
        cum_int = 0
        for alpha in alpha_list:
            this_e_a = int(alpha[0]*100+0.5)/100.
            if this_e_a >= e_a:
                cum_int += alpha[1]
        alpha_ene_cdf.append([e_a,cum_int])
        e_a -= alpha_step_size
    return alpha_ene_cdf

def run_alpha(alpha_list, mat_comp, e_alpha_step):
    binsize = 0.1 # Bin size for output spectrum

    spec_tot = {}
    xsects = {}
    total_xsect = 0
    counter = 0
    alpha_ene_cdf = condense_alpha_list(alpha_list,e_alpha_step)
    for [e_a, intensity] in alpha_ene_cdf:
        counter += 1
        if counter % (int(len(alpha_ene_cdf)/100)) == 0:
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*int(counter*100/len(alpha_ene_cdf)), 100*counter/len(alpha_ene_cdf)))
            sys.stdout.flush()

        stopping_power = 0
        if stopping_power == 0:
            stopping_power = calcStoppingPower(e_a, mat_comp)
        for mat in mat_comp:
            mat_term = getMatTerm(mat,mat_comp)
            # Get alpha n spectrum for this alpha and this target
            spec_raw = getIsotopeDifferentialNSpec(e_a, mat.ele, mat.A)
            spec = rebin(spec_raw,constants.delta_bin,constants.min_bin,constants.max_bin)
            # Add this spectrum to the total spectrum
            delta_ea = e_alpha_step
            if e_a - e_alpha_step < 0:
                delta_ea = e_a
            prefactors = (intensity/100.)*mat_term*delta_ea/stopping_power
            xsect = prefactors * readTotalNXsect(e_a,mat.ele,mat.A)
            total_xsect += xsect
            matname = str(mat.ele)+str(mat.A)
            if matname in xsects:
                xsects[matname] += xsect
            else:
                xsects[matname] = xsect
            for e in spec:
                val = prefactors * spec[e]
                if e in spec_tot:
                    spec_tot[e] += val
                else:
                    spec_tot[e] = val

    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*int((counter*100)/len(alpha_ene_cdf)), 100*(counter+1)/len(alpha_ene_cdf)))
    sys.stdout.flush()
    print('', file = sys.stdout)
    # print out total spectrum
    newspec = spec_tot
    print('',file = constants.ofile)
    print('# Total neutron yield = ', total_xsect, ' n/decay', file = constants.ofile)
    for x in sorted(xsects):
        print('\t',x,xsects[x], file = constants.ofile)
    print('# Integral of spectrum = ', integrate(newspec), " n/decay", file = constants.ofile)
    for e in sorted(newspec):
        print(e, newspec[e], file = constants.ofile)

def help_message():
    print('Usage: You must specify an alpha list or decay chain file and a target material file.\nYou may also specify a step size to for integrating the alphas as they slow down in MeV; the default value is 0.01 MeV\n\t-l [alpha list file name]\n\t-c [decay chain file name]\n\t-m [material composition file name]\n\t-s [alpha step size in MeV]\n\t-t (to run TALYS for reactions not in libraries)\n\t-d (download isotopic data for isotopes missing from database; default behavior is v2)\n\t\t-d v1 (use V1 database, TALYS-1.6)\n\t-d v2 (use V2 database, TALYS-1.95)\n\t-o [output file name]', file = sys.stdout)

def main():
    alpha_list = []
    mat_comp = []
    alpha_step_size = 0.01  #MeV (default value)
    # Load arguments
    for arg in sys.argv:
        if arg == '-l':
            alphalist_file = sys.argv[sys.argv.index(arg)+1]
            print('load alpha list', alphalist_file, file = sys.stdout)
            alpha_list = loadAlphaList(alphalist_file)
        if arg == '-c':
            chain_file = sys.argv[sys.argv.index(arg)+1]
            print('load alpha chain', chain_file, file = sys.stdout)
            alpha_list = loadChainAlphaList(chain_file)
        if arg == '-m':
            mat_file = sys.argv[sys.argv.index(arg)+1]
            print('load target material', mat_file, file = sys.stdout)
            mat_comp = readTargetMaterial(mat_file)            
        if arg == '-s':
            alpha_step_size = float(sys.argv[sys.argv.index(arg)+1])
            print('step size', alpha_step_size, file = sys.stdout)
        if arg == '-h':
            help_message()
            return 0
        if arg == '-t':
            constants.run_talys = True
        if arg == '-d':
            constants.download_data = True
            constants.download_version = 2
            version_choice = sys.argv[sys.argv.index(arg)+1]
            if (not version_choice[0] == '-') and (version_choice[0].lower() == 'v'):
                version_num = int(version_choice[1])
                constants.download_version = version_num
                print('Downloading data from version',version_num)
        if arg == '--print-alphas':
            constants.print_alphas = True
        if arg == '--print-alphas-only':
            print('Only printing alphas', file = sys.stdout)
            constants.print_alphas = True
            constants.run_alphas = False
        if arg == '--force-recalculation':
            constants.force_recalculation = True
        if arg == '-o':
            ofile = str(sys.argv[sys.argv.index(arg)+1])
            print('Printing output to',ofile, file = sys.stdout)
            constants.ofile = open(ofile,'w')
            #sys.stdout = open(ofile,'w')

    if len(alpha_list) == 0 or len(mat_comp) == 0:
        if len(alpha_list)==0: print('No alpha list or chain specified', file = sys.stdout)
        if len(mat_comp)==0: print('No target material specified', file = sys.stdout)
        print('', file = sys.stdout)
        help_message()
        return 0

    if constants.print_alphas:
        print('Alpha List: ', file = sys.stdout)
        print(max(alpha_list), file = sys.stdout)
        condense_alpha_list(alpha_list,alpha_step_size)
        for alph in alpha_list:
            print(alph[0],'&', alph[1],'\\\\', file = sys.stdout)

    if constants.download_data:
        for mat in mat_comp:
            ele = mat.ele
            if not os.path.exists('./Data/Isotopes/'+ele.capitalize()):
                if constants.download_version == 2:
                    print('\tDownloading (datset V2) data for',ele, file = sys.stdout)
                    bashcmd = './Scripts/download_element.sh ' + ele
                    process = subprocess.call(bashcmd,shell=True)
                elif constants.download_version == 1:
                    print('\tDownloading (dataset V1) data for',ele, file = sys.stdout)
                    bashcmd = './Scripts/download_element_v1.sh ' + ele
                    process = subprocess.call(bashcmd,shell=True)

    if constants.run_alphas:
        print('Running alphas:', file = sys.stdout)
        run_alpha(alpha_list, mat_comp, alpha_step_size)

if __name__ == '__main__':
    main()

