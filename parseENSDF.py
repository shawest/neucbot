#!/usr/bin/python3
import sys
from neucbot import ensdf

def main(argv):
    if(len(argv) != 3):
        print('Usage: ./parseENSDF [element] [A]')
        return

    ele = argv[1]
    A = int(argv[2])

    ensdf.Client(ele, A).write_alpha_files()

if __name__ == "__main__":
    main(sys.argv)
