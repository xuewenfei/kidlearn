#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getopt
import kidlearn_lib as k_lib
import json
import os


def main(argv):
    inputfile = ''
    stud_id = ''
    last_result = ''

    opts, args = getopt.getopt(argv, "hi:o:r:", ["ifile=", "stud_id=", "res="])
    for opt, arg in opts:
        print opt, arg
        if opt == '-h':
            print 'test.py -i <inputfile> -o <stud_id>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--l_ex"):
            stud_id = arg
        elif opt in ("-r", "--r"):
            last_result = float(arg)

    file_lex = "exlist_{}.json".format(stud_id)
    file_lastact = "last_act_{}.json".format(stud_id)

    path_dir_lex = "stud_list_ex/"
    if not os.path.exists(path_dir_lex):
        os.makedirs(path_dir_lex)

    path_file_lex = path_dir_lex + file_lex
    path_file_lastact = path_dir_lex + file_lastact

    try:
        with open(path_file_lex, 'r') as f:
            list_ex = json.load(f)
    except:
        list_ex = []

    print last_result
    if last_result != '':
        with open(path_file_lastact, 'r') as f:
            last_act = json.load(f)
        last_result = {"act": last_act, "res": last_result}
        list_ex.append(last_result)

        with open(path_file_lex, "w") as fp:
            fp.write(json.dumps(list_ex))

    zpdes = k_lib.config.seq_manager(params_file=inputfile, directory="params_files")

    for exres in list_ex:
        zpdes.update(exres["act"], exres["res"])

    act = zpdes.sample()

    with open(path_file_lastact, "w") as fp:
        fp.write(json.dumps(act))

    print str(act)


if __name__ == "__main__":
    main(sys.argv[1:])
