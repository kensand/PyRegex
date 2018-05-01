import argparse
import sys
from Regex import Regex

#The main grep function
def grep():
    parser = argparse.ArgumentParser(description="Python implementation of grep using an iterative NFA")
    parser.add_argument('regex')
    parser.add_argument('-f', '--file', nargs='*', dest='file')
    parser.add_argument('-ns', '--no-split', action='store_const', default=True, const=False, dest='split')
    parser.add_argument('-m', '--match', action='store_const', default=False, const=True, dest='match')
    parser.add_argument('-v', action='store_const', default=False, const=True, dest='verbose')
    args = parser.parse_args()
    print("'" + args.regex + "'")
    reg = args.regex
    if args.match:
        reg = ".*" + reg + ".*"
    r = Regex(reg, verbose=args.verbose)
    # print("Compiled regex.")

    if args.file is None:
        instr = sys.stdin.read()
        if args.split:
            lines = instr.splitlines()
            # print(lines)
            count = 0
            for line in lines:
                if r.interpret(line):
                    print("Line " + str(count) + "::\t " + line)
        else:
            if r.interpret(instr):
                print('Accept: "' + instr + '"')

    else:
        for file in args.file:
            f = open(file, 'r')
            instr = f.read()
            if args.split:
                lines = instr.splitlines()
                # print(lines)
                count = 0
                for line in lines:
                    if r.interpret(line):
                        print(file + ": Line " + str(count) + "::\t " + line)
            else:
                if r.interpret(instr):
                    print(file + ': "' + instr + '"')


if __name__ == "__main__":
    grep()
