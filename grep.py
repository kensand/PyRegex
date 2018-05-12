import argparse
import sys
import os

from Regex import Regex

#a simple recursive function to walk the tree of a given directory, and return the full relative path of all files found in relation to the original given path.
def walk(path):
    if not os.path.exists(path):
        return []
    ret = []
    if os.path.isdir(path):
        for subpath in os.listdir(path):
            np = os.path.join(path, subpath)
            if os.path.isfile(np):
                ret.append(np)
            elif os.path.isdir(np):
                ret += walk(np)
    return ret

# The main grep function
def grep():
    #parse arguments
    parser = argparse.ArgumentParser(
        description="Python implementation of grep using an iterative NFA. Supports most of the features found here:\n https://docs.python.org/3/library/re.html")
    parser.add_argument('regex', help="The regular expression to search for.")
    parser.add_argument('-f', '--file', nargs='*', dest='file', help='The files to search in. Leave empty to search all files in current directory, and use the Recursive (-r) flag to search recursively. ')
    parser.add_argument('-ns', '--no-split', action='store_const', default=True, const=False, dest='split',
                        help="Do not split lines. Allows for multi line matching, but then the whole file is considered a single line.")
    parser.add_argument('-m', '--match', action='store_const', default=False, const=True, dest='match',
                        help="Searches for the regular expression at any point in each line (adds '.*' to beginning and end of given regex).")
    parser.add_argument('-v', '--verbose', action='store_const', default=False, const=True, dest='verbose',
                        help="Verbose NFA input processing, for debugging and testing.")
    parser.add_argument('-r', '--recurse', action='store_const', default=False, const=True, dest='recurse',
                        help="Recursively search in given paths for regular expression (only if a given path is a directory).")
    args = parser.parse_args()

    # print("'" + args.regex + "'")
    reg = args.regex
    if args.match:
        reg = ".*" + reg + ".*"
    r = Regex(reg, verbose=args.verbose)
    # print("Compiled regex.")
    filelist = []

    # if not given any files/directories, use current working directory
    if args.file is None:
        args.file = ['.']

    # generate a list of files to search in
    for path in args.file:
        if os.path.isfile(path):
            filelist.append(path)
        elif os.path.isdir(path):
            if args.recurse:
                filelist += walk(path)
            else:
                filelist += [os.path.join(path, p) for p in os.listdir(path) if os.path.isfile(os.path.join(path, p))]

    # iterate over each file in the list and search for matches in them using the regex class.
    for file in filelist:
        f = open(file, 'r')
        try:
            instr = f.read()
        except Exception as e:
            print("Error reading file: '" + str(file) + "' with exception: " + str(e))
            instr = None
        if instr is not None:
            if args.split:
                lines = instr.splitlines()
                # print(lines)
                count = 0
                for line in lines:
                    count += 1
                    if r.interpret(line):
                        print(file + ": Line " + str(count) + "::\t " + line)
            else:
                if r.interpret(instr):
                    print(file + ': "' + instr + '"')


if __name__ == "__main__":
    grep()
