#!/usr/bin/python3
import sys
from neucbot import alpha


def main(argv):
    if len(argv) != 3:
        print("Usage: ./parseENSDF [element] [A]")
        return

    ele = argv[1]
    A = int(argv[2])

    alpha.AlphaList(ele, A).write()


if __name__ == "__main__":
    main(sys.argv)
