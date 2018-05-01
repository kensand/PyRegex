import os
import argparse
import stat

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

def permstr(p):

    s = os.stat(p)[stat.ST_MODE]
    out = ""
    if stat.S_ISDIR(s):
        out += "d"
    else:
        out += "-"

    owner = (s & 0o700) >> 6
    #print(owner)
    out += intpermstr(owner)
    group = (s & 0o70) >> 3
    #print(group)
    out += intpermstr(group)
    other = s & 0o7
    #print(other)
    out += intpermstr(other)





    return out

def equalizelens(strs, pre=False, delim=" "):
    m = max([len(w) for w in strs])
    if pre:
        return [delim * (m - len(w)) + w for w in strs]
    else:
        return [w + delim * (m - len(w)) for w in strs]

def listdir(dir, all=False, size=True, hsize=False, owner=False, group=False, permissions=True, atime=False, mtime=False, ctime=False):
    items = os.listdir(dir)
    items.sort(key=str.lower)
    itemstrs = equalizelens(items)
    if size:
        sizes = equalizelens([str(os.path.getsize(item)) for item in items])

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
            if size:
                istr += sizes[i] + "  "
            istr += itemstr + "    "

            print(istr)


parser = argparse.ArgumentParser()
parser.add_argument("directories", nargs='*')
parser.add_argument('-a', '--all', dest='all', action='store_const', default=False, const=True)
parser.add_argument('-l', '--long', dest='all', action='store_const', default=False, const=True)
parser.add_argument('-h', '--human', dest='all', action='store_const', default=False, const=True)
parser.add_argument('-a', '--all', dest='all', action='store_const', default=False, const=True)
def ls():
    args = parser.parse_args()
    if len(args.directories)  == 0:
        listdir(os.getcwd(), all=args.all)
    else:
        for dir in args.directories:
            listdir(dir, all=args.all)



if __name__ == "__main__":
    ls()