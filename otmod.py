#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  ------------------------------------------------------------------------------
#  otmod.py
#  Copyright 2015 Christopher Simpkins
#  MIT license
#  ------------------------------------------------------------------------------

import sys
import os.path
import codecs
import unicodedata
import fontTools
import yaml


# ------------------------------------------------------------------------------
# [ Argument Class ]
#   all command line arguments (object inherited from Python list)
# ------------------------------------------------------------------------------
class Argument(list):
    """Argument class is a list for command line arguments.  It provides methods for positional argument parsing"""
    def __init__(self, argv):
        self.argv = argv
        list.__init__(self, self.argv)

    # return argument at position specified by the 'position' parameter
    def get_arg(self, position):
        if self.argv and (len(self.argv) > position):
            return self.argv[position]
        else:
            return ""

    # return position of user specified argument in the argument list
    def get_arg_position(self, test_arg):
        if self.argv:
            if test_arg in self.argv:
                return self.argv.index(test_arg)
            else:
                return -1  # TODO: change the return code that indicates an error

    # return the argument at the next position following a user specified positional argument
    # (e.g. for argument to an option in cmd)
    def get_arg_next(self, position):
        if len(self.argv) > (position + 1):
            return self.argv[position + 1]
        else:
            return ""


def generate_outfile_path(filepath):
    filepath_list = os.path.split(filepath)
    directory_path = filepath_list[0]
    basefile_path = filepath_list[1]
    basefile_list = basefile_path.split(".")
    new_basefile_name = basefile_list[0] + "-new." + basefile_list[1]
    outfile = os.path.join(directory_path, new_basefile_name)
    return outfile


def read_utf8(filepath):
    """read_utf8() is a function that reads text in as UTF-8 NFKD normalized text strings from filepath
    :param filepath: the filepath to the text input file
    """
    try:
        f = codecs.open(filepath, encoding='utf_8', mode='r')
    except IOError as ioe:
        sys.stderr.write("[otmod.py] ERROR: Unable to open '" + filepath + "' for read.\n")
        raise ioe
    try:
        textstring = f.read()
        norm_text = unicodedata.normalize('NFKD', textstring)  # NKFD normalization of the unicode data before returns
        return norm_text
    except Exception as e:
        sys.stderr.write("[otmod.py] ERROR: Unable to read " + filepath + " with UTF-8 encoding using the read_utf8() method.\n")
        raise e
    finally:
        f.close()


def main(arguments):
    args = Argument(arguments)

    # Command line syntax + parsing
    # LONG OPTIONS: otmod.py --in <font infile path> --opentype <Open Type changes YAML path> --out <font outfile path>
    # SHORT OPTIONS: otmod.py -i <font infile path> -t <Open Type changes YAML path> -o <font outfile path>

    # font infile path
    if "--in" in args.argv:
        infile = args.get_arg_next(args.get_arg_position("--in"))
        if infile is "":
            sys.stderr.write("[otmod.py] ERROR: please define the font input file path as an argument to the --in command line option.\n")
            sys.exit(1)
    elif "-i" in args.argv:
        infile = args.get_arg_next(args.get_arg_position("-i"))
        if infile is "":
            sys.stderr.write("[otmod.py] ERROR: please define the font input file path as an argument to the -i command line option.\n")
            sys.exit(1)
    else:
        sys.stderr.write("[otmod.py] ERROR: Please include the `--in` option with an input font file defined as an argument.\n")
        sys.exit(1)

    # OpenType change YAML file path
    if "--opentype" in args.argv:
        otpath = args.get_arg_next(args.get_arg_position("--opentype"))
        if otpath is "":
            sys.stderr.write("[otmod.py] ERROR: please define the YAML OpenType changes file path as an argument to the --opentype command line option.\n")
            sys.exit(1)
    elif "-t" in args.argv:
        otpath = args.get_arg_next(args.get_arg_position("-t"))
        if otpath is "":
            sys.stderr.write("[otmod.py] ERROR: please define the YAML OpenType changes file path as an argument to the -t command line option.\n")
            sys.exit(1)
    else:
        sys.stderr.write("[otmod.py] ERROR: Please include the `--opentype` option and define it with an path argument to the YAML formatted OpenType changes file.\n")
        sys.exit(1)

    # font outfile path (allows for font name change in outfile)
    if "--out" in args.argv:
        outfile = args.get_arg_next(args.get_arg_position("--out"))
        if outfile is "":
            outfile = generate_outfile_path(infile)
    elif "-o" in args.argv:
        outfile = args.get_arg_next(args.get_arg_position("-o"))
        if outfile is "":
            outfile = generate_outfile_path(infile)
    else:
        outfile = generate_outfile_path(infile)

    # Test for existing file paths
    if not os.path.isfile(infile):
        sys.stderr.write("[otmod.py] ERROR: Unable to locate font at the infile path '" + infile + "'.\n")
        sys.exit(1)
    if not os.path.isfile(otpath):
        sys.stderr.write("[otmod.py] ERROR: Unable to locate the OpenType modification settings YAML file at '" + otpath + "'.\n")
        sys.exit(1)

    # Read in YAML file and convert to Python object
    try:
        pass
    except Exception as e:
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        sys.stderr.write("[otmod.py] ERROR: no arguments detected in your command.\n")
        sys.exit(1)
