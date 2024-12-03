#!/usr/bin/env python3
import pyPack
import sys

def main():

    args = sys.argv[1:]
    
    pyPack.input_check(args)
    
    option = pyPack.options_map[args[0]]
    option["callback"](pyPack.options_map, args)


if __name__ == "__main__":
    main()
