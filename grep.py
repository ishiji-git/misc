import sys, re, glob, getopt

def usage():
    sys.stderr.write("Usage: grep.py [option] [pattern] [file] ...\n")
    sys.stderr.write("          available options: n, i, v")

def make_option(orgarg, optstr, default):
    option = default
    opt, restarg = getopt.getopt(orgarg, optstr)
    for o, v in opt:
        print(o, v)
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

def search_and_print(pattern, file, option, filename=None):
    count = 0
    if option["n"]:
        if filename is None:
            printf = lambda count, line : print("{c:7d}:{l}".format(c=count, l=line), end="")
        else:
            printf = lambda count, line : print(filename+":{c:d}:{l}".format(c=count, l=line), end="")
    else:
        if option["multi"] == True:
            printf = lambda count, line : print(filename+":{l}".format(l=line), end="")
        else:
            printf = lambda count, line : print("{l}".format(l=line), end="")

    while True:
        line = file.readline()
        if line == "":
            break
        count = count + 1
        if pattern.search(line):
            if option["v"] == False:
                printf(count, line)
        else:
            if option["v"] == True:
                printf(count, line)

def grep(argv):
    """
    grep main function:
      argv is a list of grep command line argments
    """
    default_file_encoding = "cp932"

    try:
        option, restarg = make_option(argv, "inv", {"i":False,"n":False,"v":False, "multi":False})
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
    pattern = re.compile(pattern_str, flag)

    files = []
    for f in filelist:
        files = files + glob.glob(f)
    files = list(sorted(set(files)))

    filenum = len(files)
    if filenum == 0:
        search_and_print(pattern, sys.stdin, option)
    else:
        if filenum > 1:
            option["multi"] = True
        else:
            option["multi"] = False
        for f in files:
            try:
                file = open(f, "r", encoding=default_file_encoding, errors="ignore")
                search_and_print(pattern, file, option, filename=f)
                file.close()
            except Exception as err:
                sys.stderr.write("file i/o error {0}: {1}\n".format(f, str(err)))
                file.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    grep(sys.argv[1:])




