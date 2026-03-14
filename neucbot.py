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
    run_talys  = False
    run_alphas = True
    print_alphas = False
    download_data = False
    download_version = 2
    force_recalculation = False
    ofile = sys.stdout

def run_alpha(alpha_list, mat_comp, e_alpha_step):
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

        stopping_power = mat_comp.stopping_power(e_a)

        for mat in mat_comp.materials:
            mat_term = mat.material_term()
            # Get alpha n spectrum for this alpha and this target
            spec = mat.differential_n_spec(e_a, constants.run_talys, constants.force_recalculation).rebin()

            # Add this spectrum to the total spectrum
            delta_ea = e_alpha_step
            if e_a - e_alpha_step < 0:
                delta_ea = e_a
            prefactors = (intensity/100.)*mat_term*delta_ea/stopping_power
            xsect = prefactors * mat.cross_section(e_a)
            total_xsect += xsect
            matname = str(mat.element.symbol)+str(mat.mass_number)

            xsects[matname] = xsects.get(matname, 0) + xsect
            for e in spec.keys():
                spec_tot[e] = spec_tot.get(e, 0) + prefactors * spec.get(e)

    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%" % ('='*int((counter*100)/len(alpha_ene_cdf)), 100*(counter+1)/len(alpha_ene_cdf)))
    sys.stdout.flush()

    print('',file = constants.ofile)
    print('# Total neutron yield = ', utils.format_float(total_xsect), ' n/decay', file = constants.ofile)

    for x in sorted(xsects):
        print('\t', x, utils.format_float(xsects[x]), file = constants.ofile)

    print('# Integral of spectrum = ', utils.format_float(utils.Histogram(spec_tot).integrate()), " n/decay", file = constants.ofile)
    for e in sorted(spec_tot):
        print(e, utils.format_float(spec_tot[e]), file = constants.ofile)

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
            if not (os.listdir(mat.talys_output_dir()) and os.listdir(mat.talys_spectra_dir())):
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
