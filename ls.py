# File: ls.py
# A simple program to emulate the functionality of the "ls" command found in unix shells using python.


import argparse
import os
import stat
import sys
import time


# convert int to a permission string
def intpermstr(i):
    ret = ''
    if i & 4:
        ret += 'r'
    else:
        ret += '-'
    if i & 2:
        ret += 'w'
    else:
        ret += '-'
    if i & 1:
        ret += 'x'
    else:
        ret += '-'
    return ret


# gennerate permission string for a path p
def permstr(p):
    s = os.stat(p)[stat.ST_MODE]
    out = ""
    if stat.S_ISDIR(s):
        out += "d"
    else:
        out += "-"

    owner = (s & 0o700) >> 6
    # print(owner)
    out += intpermstr(owner)
    group = (s & 0o70) >> 3
    # print(group)
    out += intpermstr(group)
    other = s & 0o7
    # print(other)
    out += intpermstr(other)

    return out


# equalize the lengths of a set of strings - for nice formatting
def equalizelens(strs, pre=False, delim=" "):
    m = max([len(w) for w in strs])
    if pre:
        return [delim * (m - len(w)) + w for w in strs]
    else:
        return [w + delim * (m - len(w)) for w in strs]


# convert a file size in bytes to an appropriate new base (megabytes, gigabytes, etc.)
def humansize(size):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while size > 1024. and i < len(units) - 1:
        size = size / 1024.
        i += 1
    return ("%.2f" % size) + " " + units[i]


# the main function for listing the contents of a path.
def listdir(dir, all=False, size=True, hsize=False, owner=False, group=False, permissions=True, atime=False,
            mtime=False, ctime=False):
    if os.path.isdir(dir):
        items = os.listdir(dir)
    elif os.path.isfile(dir):
        items = [dir]
    items.sort(key=str.lower)
    itemstrs = equalizelens(items)
    sizes = None
    if hsize:
        sizes = equalizelens([humansize(os.path.getsize(item)) for item in items])
    elif size:
        sizes = equalizelens([str(os.path.getsize(item)) + " B" for item in items])

    maxlen = max([len(w) for w in items])
    for i in range(len(items)):
        item = items[i]
        itemstr = itemstrs[i]
        istr = ''
        if item[0] == '.':
            if all:
                disp = True
            else:
                disp = False
        else:
            disp = True

        if disp:
            if permissions:
                istr += permstr(item) + "  "
            if sizes:
                istr += sizes[i] + "  "
            if sys.platform == "linux" or sys.platform == "linux2":
                import pathlib
                p = pathlib.Path(items[i])
                if owner:
                    istr += " " + str(p.owner())
                if group:
                    istr += " " + str(p.group())

            if ctime:
                istr += " Created: " + str(time.asctime(time.localtime(os.path.getctime(items[i])))) + "    "
            if mtime:
                istr += " Modified: " + str(time.asctime(time.localtime(os.path.getmtime(items[i])))) + "    "
            if atime:
                istr += " Accessed: " + str(time.asctime(time.localtime(os.path.getatime(items[i])))) + "    "

            istr += itemstr + "    "

            print(istr)


parser = argparse.ArgumentParser()
parser.add_argument("path", nargs='*', help="The path(s) to a file or directory to be listed.")
parser.add_argument('-a', '--all', dest='all', action='store_const', default=False, const=True,
                    help="Show all files, including hidden ones.")
parser.add_argument('-l', '--long', dest='long', action='store_const', default=False, const=True,
                    help="Long format, displays all possible information about each file.")
parser.add_argument('-u', '--human', dest='human', action='store_const', default=False, const=True,
                    help="Show human readable file sizes.")
parser.add_argument('-s', '--size', dest='size', action='store_const', default=False, const=True,
                    help="Show file sizes in bytes.")
parser.add_argument('-o', '--owner', dest='owner', action='store_const', default=False, const=True,
                    help="Show owner of files or directories (only available on linux systems).")
parser.add_argument('-g', '--group', dest='group', action='store_const', default=False, const=True,
                    help="Show group that the file or directory belongs to (only available on linux systems).")
parser.add_argument('-p', '--permissions', dest='permissions', action='store_const', default=False, const=True,
                    help="Show permissions of files or directories.")

parser.add_argument('-t', '--access-time', dest='atime', action='store_const', default=False, const=True,
                    help="Show creation time of files or directories.")
parser.add_argument('-m', '--modify-time', dest='mtime', action='store_const', default=False, const=True,
                    help="Show modification time of files or directories.")
parser.add_argument('-c', '--creation-time', dest='ctime', action='store_const', default=False, const=True,
                    help="Show access time of files or directories.")


# the main function which deals with command line args
def ls():
    args = parser.parse_args()
    if len(args.path) == 0:
        listdir(os.getcwd(), all=args.all, size=(args.long or args.size), hsize=args.human,
                owner=(args.long or args.owner),
                group=(args.long or args.group), permissions=(args.long or args.permissions),
                atime=(args.long or args.atime), ctime=(args.long or args.ctime), mtime=(args.long or args.mtime))
    else:
        for dir in args.path:
            listdir(dir, all=args.all, size=(args.long or args.size), hsize=args.human, owner=(args.long or args.owner),
                    group=(args.long or args.group), permissions=(args.long or args.permissions),
                    atime=(args.long or args.atime), ctime=(args.long or args.ctime), mtime=(args.long or args.mtime))


if __name__ == "__main__":
    ls()
