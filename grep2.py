import sys, re, glob, getopt

def usage():
    sys.stderr.write("Usage: grep.py [option] [pattern] [file] ...\n")
    sys.stderr.write("          available options: n, i, v")

def make_option(orgarg, optstr, default):
    option = default
    opt, restarg = getopt.getopt(orgarg, optstr)
    for o, v in opt:
        if o == "-i":
            option["i"] = True
        elif o == "-n":
            option["n"] = True
        elif o == "-v":
            option["v"] = True
        else:
            sys.stderr.write("argument error:", o)
            raise
    return option, restarg

def make_printf(showline, multifile, filename=None):
    if showline:
        if filename is None:
            return lambda count, line : print("{c:7d}:{l}".format(c=count, l=line), end="")
        else:
            return lambda count, line : print(filename+":{c:d}:{l}".format(c=count, l=line), end="")
    else:
        if multifile:
            return lambda count, line : print(filename+":{l}".format(l=line), end="")
        else:
            return lambda count, line : print("{l}".format(l=line), end="")


def search_and_print(pattern, file, printf, invert):
    count = 0
    while True:
        line = file.readline()
        if line == "":
            break
        count = count + 1
        if pattern.search(line):
            if not invert:
                printf(count, line)
        else:
            if invert:
                printf(count, line)

def grep(argv):
    """
    grep main function:
      argv is a list of grep command line argments
    """
    default_file_encoding = "cp932"

    try:
        option, restarg = make_option(argv, "inv", {"i":False,"n":False,"v":False})
    except Exception as err:
        sys.stderr.write("Error: {0}\n".format(str(err)))
        sys.exit(1)

    if len(restarg) == 0:
        usage()
        sys.exit(1)
    pattern_str = restarg[0]
    filelist = restarg[1:]

    if option["i"]:
        flag = re.I
    else:
        flag = 0
    if option["v"]:
        invert = True
    else:
        invert = False
    if option["n"]:
        shownumber = True
    else:
        shownumber = False

    pattern = re.compile(pattern_str, flag)

    filenum = 0
    files = []
    multi = False
    if filelist:
        for f in filelist:
            files = files + glob.glob(f)
        files = list(sorted(set(files)))
        filenum = len(files)
        if filenum > 1:
            multi = True

    if filenum == 0:
        printf = make_printf(shownumber, multi)
        search_and_print(pattern, sys.stdin, printf, invert)
    else:
        for f in files:
            try:
                file = open(f, "r", encoding=default_file_encoding, errors="ignore")
                printf = make_printf(shownumber, multi, filename=f)
                search_and_print(pattern, file, printf, invert)
                file.close()
            except Exception as err:
                sys.stderr.write("file i/o error {0}: {1}\n".format(f, str(err)))
                file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    grep(sys.argv[1:])




