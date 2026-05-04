#!/usr/bin/python3
from argparse import ArgumentParser

from neucbot.alpha import AlphaList, ChainAlphaList
from neucbot import config
from neucbot import material
from neucbot.runner import NeucbotRunner


def main():
    parser = ArgumentParser(
        prog="neucbot",
        description="NeuCBOT is a tool for calculating (alpha,n) yields and neutron energy spectra for arbitrary materials under alpha exposure for arbitrary lists of alpha energies or in the presence of alpha-emitting contaminants.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--alpha-list", help="Alpha list file name")
    group.add_argument("-c", "--chain-list", help="Decay chain file name")

    parser.add_argument(
        "-m", "--material", required=True, help="Material composition file name"
    )
    parser.add_argument(
        "-s",
        "--step-size",
        type=float,
        default=0.01,
        help="Step size for integrating alphas (in MeV)",
    )
    parser.add_argument(
        "-t", "--talys", type=bool, help="Run TALYS for reactions not found in ./Data"
    )
    parser.add_argument(
        "-d",
        "--download",
        choices=["v1", "v2"],
        help="Download isotopic data for isotopes missing from database (options: %(choices)s)",
    )
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("--print-alphas", action="store_true", help="Print alpha list")
    parser.add_argument(
        "--print-alphas-only",
        action="store_true",
        help="Print alpha list without running calculations",
    )
    parser.add_argument(
        "--force-recalculation",
        action="store_true",
        help="Force recalculation of TALYS outputs",
    )
    parser.add_argument(
        "--json", action="store_true", help="Return outputs as JSON object"
    )

    args = parser.parse_args()

    cfg = config.Config(vars(args))
    cfg.validate()
    runner = NeucbotRunner(cfg)

    if args.alpha_list:
        alpha_list = AlphaList.from_filepath(args.alpha_list)
    elif args.chain_list:
        alpha_list = ChainAlphaList.from_filepath(args.chain_list)

    alpha_list.load_or_fetch()

    material_composition = material.Composition.from_file(args.material)

    if args.print_alphas or args.print_alphas_only:
        print("Alpha List: ")
        print(alpha_list.max_alpha())
        for [alpha, intensity] in alpha_list.condense(step_size):
            print(alpha, "&", intensity, "\\\\")

    if args.download:
        material_composition.download_data(args.download)

    runner.run(alpha_list, material_composition, args.step_size)


if __name__ == "__main__":
    main()
