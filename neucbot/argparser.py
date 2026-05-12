from argparse import ArgumentParser

argparser = ArgumentParser(
    prog="neucbot",
    description="NeuCBOT is a tool for calculating (alpha,n) yields and neutron energy spectra for arbitrary materials under alpha exposure for arbitrary lists of alpha energies or in the presence of alpha-emitting contaminants.",
)

####################
# Required Arguments
# ------------------
# 1. Each call must include either an alpha list OR a chain list, but not both
# 2. Each call must also include a material composition
####################
group = argparser.add_mutually_exclusive_group(required=True)
group.add_argument("-l", "--alpha-list", help="Alpha list file name")
group.add_argument("-c", "--chain-list", help="Decay chain file name")

argparser.add_argument(
    "-m", "--material", required=True, help="Material composition file name"
)

####################
# Optional Arguments
# ------------------
# 1. Alpha step size
# 2. Run talys during calculations
# 3. Force recalculation for talys
# 4. Download missing TALYS data
####################
argparser.add_argument(
    "-s",
    "--step-size",
    type=float,
    default=0.01,
    help="Step size for integrating alphas (in MeV)",
)

argparser.add_argument(
    "-t",
    "--talys",
    action="store_true",
    help="Run TALYS for reactions not found in ./Data",
)

argparser.add_argument(
    "--force-recalculation",
    action="store_true",
    help="Force recalculation of TALYS outputs",
)

argparser.add_argument(
    "-d",
    "--download",
    choices=["v1", "v2"],
    help="Download isotopic data for isotopes missing from database (options: %(choices)s)",
)

###########################
# Display-related Arguments
# -------------------------
# 1. output - The name of the output file to print neucBOT outputs to
# 2. Print the list of alpha energies in addition to the neucBOT outputs
# 3. ONLY print the alpha energies, skip the neucBOT calculations
# 4. Return outputs as a JSON object, rather than printing outputs. Useful in web context
###########################
argparser.add_argument("-o", "--output", help="Output file name")

argparser.add_argument("--print-alphas", action="store_true", help="Print alpha list")

argparser.add_argument(
    "--print-alphas-only",
    action="store_true",
    help="Print alpha list without running calculations",
)
argparser.add_argument(
    "--json", action="store_true", help="Return outputs as JSON object"
)
