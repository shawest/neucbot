#!/usr/bin/python3

import sys
import os
sys.path.insert(0, './Scripts/')
import subprocess

from argparse import ArgumentParser
from tqdm import tqdm

from neucbot.alpha import AlphaList, ChainAlphaList
from neucbot import material
from neucbot import talys
from neucbot import utils

class constants:
    run_talys  = False
    download_data = False
    download_version = 2
    force_recalculation = False
    ofile = sys.stdout

def run_alpha(alpha_list, mat_comp, e_alpha_step=0.01):
    spec_tot = {}
    xsects = {}
    total_xsect = 0
    for [e_a, intensity] in tqdm(alpha_list.condense(e_alpha_step)):
        stopping_power = mat_comp.stopping_power(e_a)

        for mat in mat_comp.materials:
            mat_term = mat.material_term()
            # Get alpha n spectrum for this alpha and this target
            spec = mat.differential_n_spec(e_a, constants.run_talys, constants.force_recalculation).rebin()

            # Add this spectrum to the total spectrum
            delta_ea = e_a if e_alpha_step > e_a else e_alpha_step
            prefactors = (intensity/100.)*mat_term*delta_ea/stopping_power
            xsect = prefactors * mat.cross_section(e_a)
            total_xsect += xsect

            xsects[mat.name()] = xsects.get(mat.name(), 0) + xsect
            for e in spec.keys():
                spec_tot[e] = spec_tot.get(e, 0) + prefactors * spec.get(e)

    print('',file = constants.ofile)
    print('# Total neutron yield = ', utils.format_float(total_xsect), ' n/decay', file = constants.ofile)

    for x in sorted(xsects):
        print('\t', x, utils.format_float(xsects[x]), file = constants.ofile)

    print('# Integral of spectrum = ', utils.format_float(utils.Histogram(spec_tot).integrate()), " n/decay", file = constants.ofile)
    for e in sorted(spec_tot):
        print(e, utils.format_float(spec_tot[e]), file = constants.ofile)

def main():
    alpha_list = []
    mat_comp = []

    parser = ArgumentParser(
            prog="neucbot",
            description="NeuCBOT is a tool for calculating (alpha,n) yields and neutron energy spectra for arbitrary materials under alpha exposure for arbitrary lists of alpha energies or in the presence of alpha-emitting contaminants."
            )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--alpha-list", help="Alpha list file name")
    group.add_argument("-c", "--chain-list", help="Decay chain file name")

    parser.add_argument("-m", "--material", required=True, help="Material composition file name")
    parser.add_argument("-s", "--step-size", type=float, default=0.01, help="Step size for integrating alphas (in MeV)")
    parser.add_argument("-t", "--talys", type=bool, help="Run TALYS for reactions not found in ./Data")
    parser.add_argument("-d", "--download", choices=["v1", "v2"], help="Download isotopic data for isotopes missing from database (options: %(choices)s)")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("--print-alphas", action="store_true", help="Print alpha list")
    parser.add_argument("--print-alphas-only", action="store_true", help="Print alpha list without running calculations")
    parser.add_argument("--force-recalculation", action="store_true", help="Force recalculation of TALYS outputs")

    args = parser.parse_args()

    if args.alpha_list:
        alpha_list = AlphaList.from_filepath(args.alpha_list)
    elif args.chain_list:
        alpha_list = ChainAlphaList.from_filepath(args.chain_list)

    alpha_list.load_or_fetch()

    material_composition = material.Composition.from_file(args.material)

    if args.talys:
        constants.run_talys = True

    if args.print_alphas or args.print_alphas_only:
        print('Alpha List: ', file = sys.stdout)
        print(max(alpha_list.alphas), file = sys.stdout)
        for [alpha, intensity] in alpha_list.condense(args.step_size):
            print(alpha,'&', intensity,'\\\\', file = sys.stdout)

    if args.print_alphas_only:
        return

    if args.download:
        for mat in material_composition.materials:
            if not (os.listdir(mat.talys_output_dir()) and os.listdir(mat.talys_spectra_dir())):
                print(f"Downloading (datset {args.download}) data for {mat.element.symbol}", file = sys.stdout)
                bashcmd = f"./Scripts/download_element_{args.download}.sh {mat.element.symbol}"
                process = subprocess.call(bashcmd,shell=True)

    if args.force_recalculation:
        constants.force_recalculation = True

    if args.output:
        ofile = str(args.output)
        print('Printing output to',ofile, file = sys.stdout)
        constants.ofile = open(ofile,'w')

    print('Running alphas:', file = sys.stdout)
    run_alpha(alpha_list, material_composition, args.step_size)

if __name__ == '__main__':
    main()
