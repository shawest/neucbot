#!/usr/bin/python3

import sys
import os
sys.path.insert(0, './Scripts/')
import subprocess

from neucbot import alpha
from neucbot import material
from neucbot import talys
from neucbot import utils

class constants:
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

def run_alpha(alpha_list, mat_comp, e_alpha_step):
    binsize = 0.1 # Bin size for output spectrum

    spec_tot = {}
    xsects = {}
    total_xsect = 0
    counter = 0
    alpha_ene_cdf = alpha_list.condense(e_alpha_step)
    for [e_a, intensity] in alpha_ene_cdf:
        counter += 1
        if counter % (int(len(alpha_ene_cdf)/100)) == 0:
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*int(counter*100/len(alpha_ene_cdf)), 100*counter/len(alpha_ene_cdf)))
            sys.stdout.flush()

        stopping_power = 0
        if stopping_power == 0:
            stopping_power = mat_comp.stopping_power(e_a)
        for mat in mat_comp.materials:
            mat_term = mat.material_term()
            # Get alpha n spectrum for this alpha and this target
            spec_raw = mat.differential_n_spec(e_a, constants.run_talys, constants.force_recalculation)
            spec = rebin(spec_raw,constants.delta_bin,constants.min_bin,constants.max_bin)
            # Add this spectrum to the total spectrum
            delta_ea = e_alpha_step
            if e_a - e_alpha_step < 0:
                delta_ea = e_a
            prefactors = (intensity/100.)*mat_term*delta_ea/stopping_power
            xsect = prefactors * mat.cross_section(e_a)
            total_xsect += xsect
            matname = str(mat.element.symbol)+str(mat.mass_number)
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

    rounded_total_xsect = utils.format_float(total_xsect)
    print('# Total neutron yield = ', rounded_total_xsect, ' n/decay', file = constants.ofile)

    for x in sorted(xsects):
        rounded_xsect = utils.format_float(xsects[x])
        print('\t',x,rounded_xsect, file = constants.ofile)

    rounded_integral = utils.format_float(integrate(newspec))
    print('# Integral of spectrum = ', rounded_integral, " n/decay", file = constants.ofile)
    for e in sorted(newspec):
        rounded_newspec = utils.format_float(newspec[e])
        print(e, rounded_newspec, file = constants.ofile)

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
            alpha_list = alpha.AlphaList.from_filepath(alphalist_file)
            alpha_list.load_or_fetch()
        if arg == '-c':
            chain_file = sys.argv[sys.argv.index(arg)+1]
            print('load alpha chain', chain_file, file = sys.stdout)
            alpha_list = alpha.ChainAlphaList.from_filepath(chain_file)
            alpha_list.load_or_fetch()
        if arg == '-m':
            mat_file = sys.argv[sys.argv.index(arg)+1]
            print('load target material', mat_file, file = sys.stdout)
            mat_comp = material.Composition.from_file(mat_file)
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
            print("Option set: Download data")
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

    if len(alpha_list.alphas) == 0 or mat_comp.empty():
        if len(alpha_list.alphas)==0: print('No alpha list or chain specified', file = sys.stdout)
        if mat_comp.empty(): print('No target material specified', file = sys.stdout)
        print('', file = sys.stdout)
        help_message()
        return 0

    if constants.print_alphas:
        print('Alpha List: ', file = sys.stdout)
        print(max(alpha_list.alphas), file = sys.stdout)
        condensed = alpha_list.condense(alpha_step_size)
        for alph in condensed:
            print(alph[0],'&', alph[1],'\\\\', file = sys.stdout)

    if constants.download_data:
        for mat in mat_comp.materials:
            ele = mat.element.symbol
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
