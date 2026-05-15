#!/usr/bin/python3
from neucbot.alpha import AlphaList, ChainAlphaList
from neucbot import config
from neucbot import material
from neucbot.argparser import argparser
from neucbot.runner import NeucbotRunner


def main():
    args = argparser.parse_args()

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
        for [alpha, intensity] in alpha_list.condense(args.step_size):
            print(alpha, "&", intensity, "\\\\")

        if args.print_alphas_only:
            return

    if args.download:
        material_composition.download_data(args.download)

    runner.run(alpha_list, material_composition, args.step_size)


if __name__ == "__main__":
    main()
