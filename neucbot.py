#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, './Scripts/')    # vscode suggests better solution via adding './Scripts' to extraPass
import subprocess
import shutil

# pip install sgmllib3k
import parseENSDF as ensdf  # type: ignore 

import getNaturalIsotopes as gni    # type: ignore 
import getAbundance as isoabund # type: ignore 

# pip install matplotlib
import matplotlib.pyplot as plt # type: ignore 

import re
import math
from Scripts import getNaturalIsotopes as gni
from Scripts import parseENSDF as ensdf
from Scripts import getAbundance as isoabund


class constants:
    N_A = 6.0221409e+23
    MeV_to_keV = 1_000
    mb_to_cm2 = 1.e-27
    year_to_s = 31_536_000
    min_bin = 0     # keV
    max_bin = 20_000 # keV
    delta_bin = 100 # keV
    run_talys = False
    run_alphas = True
    print_alphas = False
    calculate_energy_loss = False
    download_data = False
    download_version = 2
    force_recalculation = False
    ofile = sys.stdout


class material:
    def __init__(self, e, a, f, b):
        self.ele = str(e)
        self.A = float(a)
        self.frac = float(f)
        self.basename = str(b)
        self.num_density = constants.N_A*float(f)*1/float(a)

    def get_list(self):
        return [self.ele, self.A, self.frac, self.basename]
    
    def __str__(self):
        # This method defines the string representation of the object.
        return f"(name={self.ele}, A={self.A}, f={self.frac})"
    
    def __repr__(self):
        # This method is used for debugging and developer-focused representation.
        return f"({self.ele!r}, {self.A!r}, {self.frac!r})"


def isoDir(ele, A): # example './Data/Isotopes/Be/Be9/'
    with open(r'./Data/routes.txt', 'r') as file:
        return file.readlines()[14].rstrip()+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'


def save(name='', fmt='png'):
    pwd = os.getcwd()
    iPath = './Pictuers/'
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig(name)
    os.chdir(pwd)


def parseIsotope(iso):  # returns [ele, A]
    ele = ''
    A = 0
    for i in iso:
        if i.isalpha():
            ele += i
        if i.isdigit():
            A = A*10 + int(i)
    return [ele, A]


def generateAlphaFileName(ele, A):  # returns fName
    outdir = './AlphaLists/'
    fName = outdir + ele.capitalize() + str(A) + 'Alphas.dat'
    return fName


def generateAlphaList(ele, A):
    print('generateAlphaList(', ele, A, ')', file=constants.ofile)  
    ensdf.main(['parseENSDF', ele, A])


def loadAlphaList(fname):   # return alpha_list - [[energy]; [intensity]]
    f = open(fname) # example: fname = ./AlphaLists/Th232Alphas.dat
    tokens = [line.split() for line in f.readlines()]
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


def getAlphaList(ele, A):
    # example: fName = ./AlphaLists/Th232Alphas.dat
    fname = generateAlphaFileName(ele, A)
    return loadAlphaList(fname)


def getAlphaListIfExists(ele, A):
    # example: fName = ./AlphaLists/Th232Alphas.dat
    fName = generateAlphaFileName(ele, A)
    tries = 3
    while not os.path.isfile(fName):
        if tries < 0:
            print('Cannot generate alpha list for ele =', ele, ' and A =', A, file=constants.ofile)
            return 0
        print('generating alpha file', fName, file=constants.ofile)
        generateAlphaList(ele, A) 
        tries -= 1 
    return getAlphaList(ele, A)


def loadChainAlphaList(fname):  # returns list [E_alpha, Intesity] for each isotop in chain 
    f = open(fname) # fname = Chains/Th232Chain.dat 
    tokens = [line.split() for line in f.readlines()] 
    alpha_list = [] 
    for line in tokens: 
        if len(line) < 2 or line[0][0] == '#': 
            continue 

        # Read isotope and its branching ratio from file
        iso = line[0]   # element + atomic mass
        br = float(line[1])  # Branching
        [ele, A] = parseIsotope(iso)  # example: iso='Th232' --> ele='Th', A=232

        # Now get the isotope's alpha list and add it to the chain's list 
        aList_forIso = getAlphaListIfExists(ele, A) 
        if constants.print_alphas:
            print(iso, file = constants.ofile) 
            print('\t', aList_forIso, file = constants.ofile)
        for [ene, intensity] in aList_forIso:
            alpha_list.append([ene, intensity*br / 100])    #why multiply the branching ratio by intensity?
    return alpha_list


def readTargetMaterial(fname):
    f = open(fname) # example: fname = Materials/Acrylic.dat
    mat_comp = []
    tokens = [line.split() for line in f.readlines()]

    for line in tokens:  
        # File contains a table of four columns: 
        # element name,
        # atomic mass number, 
        # the percentage of mass of the element in the material,
        # data base name: j - JENDL; t - TALYS.

        if len(line) < 3:
            continue
        if line[0][0] == '#':
            continue
        ele = line[0].lower()
        A = int(line[1])
        frac = float(line[2])
        basename = line[3].lower() if len(line) == 4 else 't'

        if A == 0:
            # mass number of ele
            natIso_list = gni.findIsotopes(ele).split()
            for A_i in natIso_list:  # 
                # finding abundance of isotope A_i + ele (13C)
                abund = float(isoabund.findAbundance(
                    str(A_i)+ele.capitalize()))
                # structure 'mater' contains element name (C), atomic mass (13),
                # mass fraction of isotope (C13) and basename (j/t).
                mater = material(ele, A_i, frac*abund/100., basename)
                mat_comp.append(mater)
        else:
            mater = material(ele, A, frac, basename)
            mat_comp.append(mater)

    # Normalize
    norm = 0
    for mat in mat_comp:
        norm += mat.frac
    for mat in mat_comp: #can condense into a single loop
        mat.frac /= norm

    return mat_comp


def calcStoppingPower(e_alpha_MeV, mat_comp):
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

        tokens = [line.split() for line in spf.readlines()]
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
                e_curr /= 1_000
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
                sp_alpha = (sp_curr-sp_last) * (e_alpha-e_last) / (e_curr-e_last) + sp_last
                sp_found = True
                break
            # Otherwise, keep looking for the entry
            first = False
            sp_last = sp_curr
            e_last = e_curr
        # if the alpha energy is too high for the list, use the highest energy on the list
        if not sp_found:
            sp_alpha = sp_last
        sp_total += sp_alpha * mat_comp_reduced[mat] / 100
    return sp_total


def runTALYS(e_a, ele, A):
    iso = str(ele)+str(int(A))
    inpdir = isoDir(ele, A) + 'TalysInputs/'
    outdir = isoDir(ele, A) + 'TalysOut/'
    nspecdir = isoDir(ele, A) + 'NSpectra/'
    if not os.path.exists(inpdir):
        os.makedirs(inpdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not os.path.exists(nspecdir):
        os.makedirs(nspecdir)

#    command = '\nprojectile a\nejectiles p n g\nelement '+ele+'\nmass '+str(int(A))+'\nenergy '+str(
#       e_a)+'\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2\n'
    command = '\nprojectile a\nejectiles p n g\nelement '+ele+'\nmass '+str(int(A))+'\nenergy '+str(
        e_a)+'\npreequilibrium y\ngiantresonance y\nmultipreeq y\noutspectra y\noutlevels y\noutgamdis y\nfilespectrum n\nelwidth 0.2'

    inp_fname = inpdir+'inputE'+str(e_a)
    inp_f = open(inp_fname, 'w')
    inp_f.write(command)
    inp_f.close()
    out_fname = outdir+'outputE'+str(e_a)

    bashcmd = 'talys < '+inp_fname+' > '+out_fname
    print('Running TALYS:\t', bashcmd, file=constants.ofile)
    runscript_fname = './runscript_temp.sh'
    runscript_f = open(runscript_fname, 'w')
    runscript_f.write('#!/usr/bin/bash\n\n'+bashcmd)
    runscript_f.close()
    process = subprocess.call(bashcmd, shell=True)
    # Move the output neutron spectrum to the appropriate directory
    ls = os.listdir('./')

    moved_file = False
    for f in ls:
        if 'nspec' in f:
            if os.path.exists(nspecdir+f):
                os.remove(nspecdir+f)
            fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
            shutil.move(f, fname)
            moved_file = True
    # If no neutron spectrum file is found, make a blank one
    if not moved_file:
        fname = nspecdir+'nspec{0:0>7.3f}.tot'.format(e_a)
        blank_f = open(fname, 'w')
        blank_f.write('EMPTY')
        blank_f.close()


def getMatTerm(mat, mat_comp):  # return N_A * C_m / A_m
    # mat_comp structure: [ele, A, frac, basename]
    # mat structure: ele, A, frac, basename
    A = mat.A
    conc = mat.frac/100.
    mat_term = (constants.N_A * conc) / A
    return mat_term


def getIsotopeDifferentialNSpecJENDL(e_a, ele, A, MT):  # return spec {energy [keV] : sigma [cm^2/MeV]}  
    # isoDir = './Data/Isotopes/'+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'
    # example: isoDir = './Data/Isotopes/C/C13/'
    path = isoDir(ele, A) + 'JendlOut/MT' + str(MT) + '/'
    fname = path + 'outputE' + str("{:.4f}".format(e_a))

    spec = {}

    if not os.path.exists(fname):
        print("NO JENDL file. e_a, ele, A, MT:", e_a, ele, A, MT)

    f = open(fname) 

    tokens = [line.split() for line in f.readlines()]
    for line in tokens:  # iterating over the E_out (= neutron energies) 
        if len(line) < 1 or line[0] == 'EMPTY':
            break
        if line[0][0] == '#':
            continue

        # line[0] = E_out in lab, eV	
        # line[1] = distribution

        energy = int(float(line[0])*constants.MeV_to_keV)   # in keV
        sigma = float(line[1]) * constants.mb_to_cm2 / constants.MeV_to_keV
        spec[energy] = sigma 
    f.close()
    return spec # cm^2/MeV


def getIsotopeDifferentialNSpec(e_a, ele, A):   # return spec {energy [keV] : sigma [cm^2/MeV]}  
    target = ele+str(int(A))
    # isoDir = './Data/Isotopes/'+ele.capitalize()+'/'+ele.capitalize()+str(int(A))+'/'
    # example: isoDir = './Data/Isotopes/C/C13/'
    path = isoDir(ele, A) + 'NSpectra/'
    if not os.path.exists(path):
        os.makedirs(path)
    fname = path+'nspec{0:0>7.3f}.tot'.format(int(100*e_a)/100.)
    # a +  13C : neutron  spectrum
    # E-incident =    4.230
    #
    # energies =   135 # (Number of lines)
    # E-out    Total       Direct   ...
    # 0.100    ...         ...      ... 
    # 0.200    ...         ...      ...

    outpath = isoDir(ele, A) + 'TalysOut'
    if constants.force_recalculation:
        print('Forcibily running TALYS for', int(100*e_a)/100., 'alpha on', target, file=constants.ofile)
        print('Outpath', outpath, file=constants.ofile)
        runTALYS(int(100*e_a)/100., ele, A)

    # If the file does not exist, run TALYS
    if not os.path.exists(fname):
        if constants.run_talys:
            while not os.path.exists(fname):
                print('Running TALYS for', int(100*e_a)/100., 'alpha on', target, file=constants.ofile)
                print('Outpath', outpath, file=constants.ofile)
                runTALYS(int(100*e_a)/100., ele, A)
                ls = os.listdir(outpath)
        else:
            print('Warning, no (alpha,n) data found for E_a =', e_a, 'MeV on target', target, '...skipping. Consider running with the -d or -t options', file=constants.ofile)
            return {}

    # Load the file
    # If no output was produced, skip this energy
    if not os.path.exists(outpath):
        return {}

    f = open(fname) # NSpectra/... 

    spec = {}
    tokens = [line.split() for line in f.readlines()]

    for line in tokens:  # line stands for E_out

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

        # convert from MeV to keV
        energy = int(float(line[0])*constants.MeV_to_keV)
        # convert from mb/MeV to cm^2/MeV
        sigma = float(line[1])*constants.mb_to_cm2 / constants.MeV_to_keV    # Divide by 10^30
        spec[energy] = sigma 
    return spec # cm^2/MeV


def rebin(histo, step, minbin, maxbin): # histo = spec_raw
    # histo - distribution of the neutron cross section by their energy output for specific alpha and nuclei
    nbins = (maxbin-minbin) / step   # Number of columns in the new spectrum
    newhisto = {}
    normhisto = {}
    for i in sorted(histo):  # i - is energy
        index = sorted(histo).index(i)  # Number of column in the spectrum
        # Get the spacing between points
        delta = sorted(histo)[0]
        if index > 0: 
            delta = sorted(histo)[index] - sorted(histo)[index-1]
        # If the x value is too low, put it in the underflow bin (-1)
        if i < minbin:
            print('Underflow:', i, ' (minbin =', minbin, ')', file=constants.ofile)
            if -1 in newhisto:
                newhisto[-1] += histo[i]*delta
                normhisto[-1] += delta
            else:
                newhisto[-1] = histo[i]*delta
                normhisto[-1] = delta
        # ...or the overflow bin if too high
        if i > maxbin:
            print('Overflow:', histo[i], ' (maxbin =', maxbin, ')', file=constants.ofile)
            overflowbin = int(nbins+10*step)
            if overflowbin in newhisto:
                newhisto[overflowbin] += histo[i]*delta
                normhisto[overflowbin] += delta
            else:
                newhisto[overflowbin] = histo[i]*delta
                normhisto[overflowbin] = delta
        # Otherwise, calculate the bin
        # New bin size is a multiple of delta_bin=100keV
        newbin = int(minbin+(int((i-minbin) / step)*step))
        if newbin in newhisto:  # newhisto has delta_bin = 100keV
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


def readTotalNXsectJENDL(e_a, ele, A, MT): # return JENDL XS of (a,n) reaction in cm2

    dirname = isoDir(ele, A) + 'JendlOut'

    # dirname = isoDir(ele, A) + 'MohrOut'
    # if e_a > 7.96:
    #     dirname = isoDir(ele, A) + 'JendlOut'

    fname = dirname + '/MT' + str(MT) + '/cross-section' 
    f = open(fname) 
    lines = [line.split() for line in f.readlines()] 
    sigma = 0
    for line in lines:  # This two 'if's make JENDL-powered neucbot much slower!!!
        if (line[0] != '#'):
            if e_a >= float(line[0]):   
                sigma = float(line[1])*constants.mb_to_cm2
                # break
    f.close()
    return sigma    # XS in cm2


def readTotalNXsect(e_a, ele, A): # return TALYS XS of (a,n) reaction in cm2
    
    fname = isoDir(ele, A) + 'TalysOut/outputE' + str(int(100*e_a)/100.)
    if not os.path.exists(fname):
        print('Could not find file', fname, file=constants.ofile)
        return 0
    f = open(fname)
    lines = [line.split() for line in f.readlines()]

    xsect_line = 0
    for line in lines:  # Looking for particular line in file '.../TalysOut/outputE...'
        if line == ['2.', 'Binary', 'non-elastic', 'cross', 'sections', '(non-exclusive)']:
            break
        else:
            xsect_line += 1

    xsect_line += 3 # (a,n) XS is stored three lines below the line 
                    # '2. Binary non-elastic cross sections (non-exclusive)'
    if len(lines) < xsect_line:
        return 0
    if lines[xsect_line][0] != 'neutron':
        return 0
    sigma = float(lines[xsect_line][2])  # (a,n) XS in mb (= 10^-27 cm2)
    sigma *= constants.mb_to_cm2    
    f.close()

    # f = open('talys_XS_print', 'a+')
    # f.write(str(e_a) + '\t' + str(sigma / constants.mb_to_cm2) + '\n')
    # f.close()

    return sigma    # XS in cm2


def condense_alpha_list(alpha_list, alpha_step_size):
    # alpha_list - list of alpha particles with probability of each in decay chain.
    alpha_ene_cdf = []  # cdf - cumulative distribution function
    max_alpha = max(alpha_list)

    e_a_max = int(max_alpha[0]*100 + 0.5)/100.  # Rounds up the energy. Could be done via 'floor()'
    alpha_ene_cdf.append([e_a_max, max_alpha[1]])
    e_a = e_a_max
    while e_a > 0:  # Summ up all the probabilities of alpha particles with energy less than e_a.

        cum_int = 0
        for alpha in alpha_list:
            this_e_a = int(alpha[0]*100+0.5)/100.
            if this_e_a >= e_a:
                cum_int += alpha[1]
        alpha_ene_cdf.append([e_a, cum_int])
        e_a -= alpha_step_size
    return alpha_ene_cdf


def calculate_num_steps(alpha_list,alpha_step_size):
    total_steps = 0
    for alpha in alpha_list:
        this_e_a = int(alpha[0]*100 + .05)/100
        total_steps += int((this_e_a/alpha_step_size)*100)/100
    return total_steps


def n_prob_spec(nspec, total):
    prob_spec = {}
    for e in nspec:
        probability = (nspec[e]/total) * 100 * 100
        prob_spec[e] = probability
    return prob_spec


def download_talys_data(mat_comp):
    for mat in mat_comp:
        ele = mat.ele
        if not os.path.exists('UI/Data/Isotopes/'+ele.capitalize()):
            if constants.download_version == 2:
                print('\tDownloading (datset V2) data for',ele, file = sys.stdout)
                bashcmd = './UI/Scripts/download_element.sh ' + ele
                process = subprocess.call(bashcmd,shell=True)
            elif constants.download_version == 1:
                print('\tDownloading (dataset V1) data for',ele, file = sys.stdout)
                bashcmd = './UI/Scripts/download_element_v1.sh ' + ele
                process = subprocess.call(bashcmd,shell=True)


def run_alpha_energy_loss(alpha_list, mat_comp, e_alpha_step):
    binsize = 0.1 # Bin size for output spectrum
    spec_tot = {}
    xsects = {}
    total_xsect = 0
    counter = 0
    total_steps = (calculate_num_steps(alpha_list, e_alpha_step)*100+.5)/100
    nprob_spectrum = {}
    a_n_spec = {}
    a_n_probspec = {}
    a_n_probspec_norm = {}
    a_n_mat_probspec = {}
    #iterate through each alpha in the alpha list
    
    for [e_a, intensity] in alpha_list:
        this_e_a = int(e_a*100+.5)/100

        #iterate through entire alpha's energy
        #delta_e_a = 0
        while this_e_a > 0:
            counter += 1

            #loading bar
            if counter % (int(total_steps/100)) == 0:
                sys.stdout.write('\r')
                sys.stdout.write("[%-100s] %d%%" % ('='*int(counter*100/total_steps), 100*counter/total_steps))
                sys.stdout.flush()

            #calculate stopping power for this alpha energy
            stopping_power = calcStoppingPower(this_e_a, mat_comp)
            
            #iterate through each material for each change in energy
            for mat in mat_comp:
                #calculate total cross section at this energy
                mat_term = getMatTerm(mat,mat_comp)
                prefactors = (intensity/100.)*mat_term*e_alpha_step/stopping_power
                xsect = prefactors*readTotalNXsect(this_e_a, mat.ele,mat.A)
                total_xsect += xsect

                #calculate neutron spectrum at this energy
                spec_raw = getIsotopeDifferentialNSpec(this_e_a, mat.ele, mat.A)
                spec = rebin(spec_raw, constants.delta_bin, constants.min_bin, constants.max_bin)
                matname = str(mat.ele)+str(mat.A)

                #calculate spectrum for each material
                if matname in xsects:
                    xsects[matname] += xsect
                else:
                    xsects[matname] = xsect

                #calculate neutron yield for each each neutron energy
                delta_e_a = round(e_a - this_e_a, 2)
                for e in spec:
                    val = prefactors * spec[e]
                    if e in spec_tot:
                        spec_tot[e] += val
                        if (e,delta_e_a) in a_n_spec:
                            a_n_spec[e,delta_e_a] += val
                        else:
                            a_n_spec[e,delta_e_a] = val
                    else:
                        spec_tot[e] = val
                        a_n_spec[e,delta_e_a] = val

                        

            #energy step
            this_e_a -= e_alpha_step

    nspec_sum = integrate(spec_tot)
    for e in spec_tot:
        nprob_spectrum[e] = spec_tot[e]/nspec_sum

    #calculate probabilities across entire (a,n) spectrum
    for e, delta_e_a in a_n_spec:
        if spec_tot[e] == 0:
            continue
        else:
            a_n_probspec[e,delta_e_a] = a_n_spec[e,delta_e_a]/spec_tot[e]
            a_n_probspec_norm[e,delta_e_a] = a_n_spec[e,delta_e_a]/nspec_sum
    
    #make discrete lists for (a,n) graphs for each neutron energy level
    a_n_list = {}
    for e in spec_tot:
        a_n_graph = {}
        for en, delta_e_a in a_n_spec:
            if e == en and spec_tot[e] != 0:
                a_n_graph[delta_e_a] = a_n_probspec[e,delta_e_a]/constants.delta_bin
        a_n_list[e] = a_n_graph
    
    #calculate probabilities for each element
    for e, delta_e_a in a_n_spec:
        if spec_tot[e] == 0:
            continue
        else:
            a_n_mat_probspec[e,delta_e_a] = a_n_spec[e,delta_e_a]/spec_tot[e]

    #make discrete lists for (a,n) spectrum split into constituent elements
    a_n_mat_list = {}
    for e in spec_tot:
        a_n_mat_graph = {}
        for en, delta_e_a in a_n_spec:
            if e == en and spec_tot[e] != 0:
                a_n_mat_graph[delta_e_a] = a_n_mat_probspec[e,delta_e_a]
        a_n_mat_list[e,mat] = a_n_mat_graph

    #make a simple list of each alpha energy increment for later iteration in flask app
    max_alpha = round(max(alpha_list)[0], 2)
    max_alpha_list = []
    while max_alpha >= 0:
        max_alpha_list.append(max_alpha)
        max_alpha = round(max_alpha - e_alpha_step, 2)
        
    return xsects, spec_tot, nprob_spectrum, a_n_probspec, max_alpha_list, a_n_list, a_n_probspec_norm


def run_alpha(alpha_list, mat_comp, e_alpha_step):
    # alpha_list - list of alpha particles with probability of each in decay chain.
    # mat_comp - list of element name, atonic mass, mass fraction and database name.
    # e_alpha_step - bin size for input spectrum. By default, 0.01 MeV

    binsize = 0.1   # Bin size for output spectrum, MeV

    spec_tot = {} 
    xsects = {}
    # partial_spec_tot = []   # for TALYS partail code MT = 4 
    # partial_xsects = []     # for TALYS partail code MT = 4
    total_xsect = 0 
    counter = 0 

    # Calculation of the cumulative alpha particle probability distribution function.
    alpha_ene_cdf = condense_alpha_list(alpha_list, e_alpha_step)   # cdf - cumulative distribution function
    stopping_power = 0

    for [e_a, intensity] in alpha_ene_cdf:
        counter += 1
        if counter % (int(len(alpha_ene_cdf) / 100)) == 0:
            sys.stdout.write('\r')
            sys.stdout.write('[%-100s] %d%%' % ('='*int(counter*100 / len(alpha_ene_cdf)), 
                                                100*counter / len(alpha_ene_cdf)))
            sys.stdout.flush()
        
        stopping_power = calcStoppingPower(e_a, mat_comp)   # ksi(E_a)

        for mat in mat_comp:    # example: for Acryllic 'mat_comp' is [C12, C13, H1, H2, O16, O17, O18].
            
            mat_term = getMatTerm(mat, mat_comp)    # N_A * C_m / A_m

            delta_ea = e_alpha_step
            if e_a - e_alpha_step < 0:
                delta_ea = e_a
            # Part of formulae that is inside the integral.
            prefactors = ((intensity/100.) * mat_term * delta_ea )/ stopping_power

            if not os.path.exists(isoDir(mat.ele, mat.A) + 'JendlOut'): 
                # print('No such Jendl file: ', mat.ele, mat.A) 
                mat.basename = 't'

            if (mat.basename == 'j'): 
                
                # ====start==== MT = 4 ====start==== #
                
                # Get raw spec {energy [keV] : sigma [cm^2/MeV]}  
                spec_raw = getIsotopeDifferentialNSpecJENDL(e_a, mat.ele, mat.A, MT=4)
                # Rebin raw spec 
                spec = rebin(spec_raw, constants.delta_bin, constants.min_bin, constants.max_bin) 
                # Multiply prefactors[?] by XS[cm^2]
                xsect = prefactors * readTotalNXsectJENDL(e_a, mat.ele, mat.A, MT=4)
                total_xsect += xsect    # total - for material. xsect stands for each particular nuclide.
                matname = str(mat.ele)+str(int(mat.A)) 
                if matname in xsects: 
                    xsects[matname] += xsect 
                else:
                    xsects[matname] = xsect
                # xsects = {C13 : xsect}

                for e in spec:
                    val = prefactors * spec[e]
                    if e in spec_tot:
                        spec_tot[e] += val
                    else:
                        spec_tot[e] = val
                
                # =====end===== MT = 4 =====end===== #
                                        
                # dirname = isoDir(mat.ele, mat.A) + 'JendlOut' 
                # dirLen = len([name for name in os.listdir(dirname)])
                # for MT in range(dirLen-1): 
                #     partial_xsects = {} 
                #     partial_spec_tot = {} 
                #     MT += 50 
                #     partial_spec_raw = getIsotopeDifferentialNSpecJENDL(e_a, mat.ele, mat.A, MT) 
                #     partial_spec = rebin(partial_spec_raw, constants.delta_bin, constants.min_bin, constants.max_bin) 
                #     partial_xsect = prefactors * readTotalNXsectJENDL(e_a, mat.ele, mat.A, mat.basename, MT) # cm^2 
                        
                #     partial_total_xsect += partial_xsect 
                #     matname = str(mat.ele)+str(int(mat.A)) 
                #     if matname in partial_xsects: 
                #         partial_xsects[matname]+= partial_xsect 
                #     else:
                #         partial_xsects[matname] = partial_xsect

                #     for e in partial_spec:
                #         val = prefactors * partial_spec[e]
                #         if e in partial_spec_tot:
                #             partial_spec_tot[e] += val
                #         else:
                #             partial_spec_tot[e] = val
                

            if (mat.basename == 't'): 
                
                spec_raw = getIsotopeDifferentialNSpec(e_a, mat.ele, mat.A) 
                spec = rebin(spec_raw, constants.delta_bin, constants.min_bin, constants.max_bin) 
                xsect = prefactors * readTotalNXsect(e_a, mat.ele, mat.A) # cm^2 
                
                total_xsect += xsect 
                matname = str(mat.ele)+str(int(mat.A)) 
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
    sys.stdout.write('[%-100s] %d%%' % ('='*int((counter*100) / len(alpha_ene_cdf)), 100*(counter+1) / len(alpha_ene_cdf)))
    sys.stdout.flush()
    print('', file=sys.stdout)
    
    # print out total spectrum
    newspec = spec_tot

    print('',file = constants.ofile)
    print('# Total neutron yield = ', '{0:.2e}'.format(total_xsect), ' n/decay', file = constants.ofile)

    for x in sorted(xsects):
        print('\t',x,'{0:.2e}'.format(xsects[x]), file = constants.ofile)
    print('# Integral of spectrum = ', '{0:.2e}'.format(integrate(newspec)), " n/decay", file = constants.ofile)
    for e in sorted(newspec):
        formatted_e = str(e).rjust(6)  

        max_length=10
        formatted_spec = f"{newspec[e]:.{max_length}g}"
        if len(formatted_spec) > max_length:
            mantissa, exponent = formatted_spec.split('e')
            mantissa_length = max_length - len(exponent) - 2
            mantissa = mantissa[:mantissa_length]
            
            formatted_spec = f"{mantissa}e{exponent}"
        print(f'{formatted_e}', formatted_spec, file = constants.ofile)
        # print(f'{formatted_e}', '{0:.2e}'.format(newspec[e]), file = constants.ofile) # will always be 0 after a certain point?
    return xsects,newspec


def help_message():
    print('Usage: You must specify an alpha list or decay chain file and a target material file.\n\
          You may also specify a step size to for integrating the alphas as they slow down in MeV; the default value is 0.01 MeV\n\
          \t-l [alpha list file name]\n\
          \t-c [decay chain file name]\n\
          \t-m [material composition file name]\n\
          \t-s [alpha step size in MeV]\n\
          \t-t (to run TALYS for reactions not in libraries)\n\
          \t-d (download isotopic data for isotopes missing from database; default behavior is v2)\n\
          \t\t-d v1 (use V1 database, TALYS-1.6)\n\
          \t-d v2 (use V2 database, TALYS-1.95)\n\
          \t-o [output file name]', file=sys.stdout)


def main():
    alpha_list = []
    mat_comp = []
    alpha_step_size = 0.01  # 0.01 MeV (default value)
    # Load arguments
    # argv = ['neucbot.py', '-m', 'Materials/Acrylic.dat', '-c', 'Chains/Th232Chain.dat']
    for arg in sys.argv:
        # for arg in argv:
        if arg == '-l':
            alphalist_file = sys.argv[sys.argv.index(arg)+1]
            print('load alpha list', alphalist_file, file=sys.stdout)
            alpha_list = loadAlphaList(alphalist_file)

        if arg == '-c': 
            '''mat_file = sys.argv[sys.argv.index('-m')+1]
            mat_comp = readTargetMaterial(mat_file)
            if mat_comp[1] == 'j':
                continue'''
            chain_file = sys.argv[sys.argv.index(arg)+1]    # example: chain_file = Chains/Th232Chain.dat
            print('load alpha chain', chain_file, file=sys.stdout)
            alpha_list = loadChainAlphaList(chain_file)

        if arg == '-m': 
            mat_file = sys.argv[sys.argv.index(arg)+1]  # example: mat_file = Materials/Acrylic.dat
            print('load target material', mat_file, file=sys.stdout)
            mat_comp = readTargetMaterial(mat_file)
            # returns list of element name, atomic mass, mass fraction and database name.

        if arg == '-s':
            alpha_step_size = float(sys.argv[sys.argv.index(arg)+1])
            print('step size now is', alpha_step_size, file=sys.stdout)
        if arg == '-h':
            help_message()
            return 0
        if arg == '-t':
            constants.run_talys = True
        if arg == '-d':
            constants.download_data = True
            constants.download_version = 2
            if len(sys.argv) > sys.argv.index(arg)+1:
                version_choice = sys.argv[sys.argv.index(arg)+1]
                if (not version_choice[0] == '-') and (version_choice[0].lower() == 'v'):
                    version_num = int(version_choice[1])
                    constants.download_version = version_num
                    print('Downloading data from version', version_num)
        if arg == '-Ea':
            constants.calculate_energy_loss = True
        if arg == '--print-alphas':
            constants.print_alphas = True
        if arg == '--print-alphas-only':
            print('Only printing alphas', file=sys.stdout)
            constants.print_alphas = True
            constants.run_alphas = False
        if arg == '--force-recalculation':
            constants.force_recalculation = True
        if arg == '-o':
            ofile = str(sys.argv[sys.argv.index(arg)+1])
            print('Printing output to', ofile, file=sys.stdout)
            constants.ofile = open(ofile, 'w')

    if len(alpha_list) == 0 or len(mat_comp) == 0:
        if len(alpha_list) == 0:
            print('No alpha list or chain specified', file=sys.stdout)
        if len(mat_comp) == 0:
            print('No target material specified', file=sys.stdout)
        print('', file=sys.stdout)
        help_message()
        return 0

    if constants.print_alphas:
        print('Alpha List:', file=sys.stdout)
        print(max(alpha_list), file=sys.stdout)
        condense_alpha_list(alpha_list, alpha_step_size)     # why call this function?
        for alph in alpha_list:
            print(alph[0], '&', alph[1], '\\\\', file=sys.stdout)

    if constants.download_data:
        for mat in mat_comp:
            ele = mat.ele
            basename = mat.basename
            if basename == 't':
                with open(r'./Data/routes.txt', 'r') as file:
                    if not os.path.exists(file.readlines()[14].rstrip()+ele.capitalize()):
                        if constants.download_version == 2:
                            print('\tDownloading (TALYS-1.95) data for', ele, file=sys.stdout)
                            bashcmd = './Scripts/download_element.sh ' + ele
                            process = subprocess.call(bashcmd, shell=True)
                        elif constants.download_version == 1:
                            print('\tDownloading (TALYS-1.6) data for', ele, file=sys.stdout)
                            bashcmd = './Scripts/download_element_v1.sh ' + ele
                            process = subprocess.call(bashcmd, shell=True)
                        elif constants.download_version == "j":
                            print('\tDownloading (TALYS-1.6) data for', ele, file=sys.stdout)
                            bashcmd = './Scripts/download_jendl_data.sh ' + ele
                            process = subprocess.call(bashcmd, shell=True)
            else:
                with open(r'./Data/routes.txt', 'r') as file:
                    if not os.path.exists('jendl'+file.readlines()[14].rstrip()+ele.capitalize()):
                        print('ERROR: there is no folder for jendl')
                        bashcmd = './Scripts/download_element_jendl.sh '

    if constants.run_alphas:
        if constants.calculate_energy_loss:
            print('Running alphas w/ energy loss:', file = sys.stdout)
            run_alpha_energy_loss(alpha_list, mat_comp, alpha_step_size)
        else:
            print('Running alphas:', file = sys.stdout)
            run_alpha(alpha_list, mat_comp, alpha_step_size)
        # alpha_list - list of alpha particles in decay chain
        # mat_comp - list of element name, atomic mass, mass fraction and database name.


if __name__ == '__main__':
    main()
