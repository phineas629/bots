# -*- coding: utf-8 -*-

import argparse
import atexit
import collections
import copy
import glob
import logging
import os
import pickle
import sys
import unicodedata

from . import botsglobal, botsinit, botslib, grammar
from .botsconfig import ID, LEVEL, MANDATORY, MAX, MIN, SEARCH


def grammarread(editype, grammarname):
    """dispatch function for reading whole grammar"""
    read_functions = {
        "csv": cvaread,
        "fixed": fixedread,
        "idoc": idocread,
        "xml": xmlread,
        "json": jsonread,
        "template": templateread,
        "tradacoms": tradacomsread,
        "edifact": edifactread,
        "x12": x12read,
    }
    read_function = read_functions.get(editype)
    if read_function:
        return read_function(editype, grammarname)
    else:
        raise botslib.GrammarError('Grammar "{}" does not exist.'.format(editype))


def cvaread(editype, grammarname):
    """read csv grammar"""
    grdic = grammar.grammarread(editype, grammarname)
    grdic["editype"] = editype
    grdic["grammarname"] = grammarname
    # For CVS/fixed: check the grammar:
    grdic["syntax"]["noBOTSID"] = True  # there is no BOTSID in CSV records....
    if "merge" not in grdic:
        grdic["merge"] = False
    if "quote_char" not in grdic["syntax"]:
        grdic["syntax"]["quote_char"] = '"'
    return grdic


def startmulti(grammardir, editype):
    """specialized tool for bulk checking of grammars while developing botsgrammars
    grammardir: directory with grammars (e.g., bots/usersys/grammars/edifact)
    editype: e.g., edifact
    """
    configdir = "config"
    botsinit.generalinit(configdir)  # find locating of bots, configfiles, init paths etc.
    process_name = "grammarcheck"
    botsglobal.logger = botsinit.initenginelogging(process_name)
    atexit.register(logging.shutdown)

    for filename in glob.iglob(grammardir):
        filename_basename = os.path.basename(filename)
        if filename_basename in ["__init__.py", "envelope.py"]:
            continue
        if (
            filename_basename.startswith("edifact")
            or filename_basename.startswith("records")
            or filename_basename.endswith("records.py")
        ):
            continue
        if filename_basename.endswith("pyc"):
            continue
        filename_noextension = os.path.splitext(filename_basename)[0]
        try:
            grammar.grammarread(editype, filename_noextension, typeofgrammarfile="grammars")
        except Exception as e:
            print((botslib.txtexc()))
        else:
            print(("OK - no error found in grammar {}".format(filename)))


def start():
    parser = argparse.ArgumentParser(description="Bots Grammar Checker")
    parser.add_argument(
        "-c",
        "--config",
        default="config",
        help="directory for configuration files (default: config)",
    )
    parser.add_argument("editype", nargs="?", help="editype")
    parser.add_argument("messagetype", nargs="?", help="messagetype")
    parser.add_argument("filepath", nargs="?", help="path to grammar file")
    args = parser.parse_args()

    if args.filepath and os.path.isfile(args.filepath):
        p1, p2 = os.path.split(args.filepath)
        editype = os.path.basename(p1)
        messagetype, _ = os.path.splitext(p2)
        print(("grammarcheck", editype, messagetype))
    elif args.editype and args.messagetype:
        editype = args.editype
        messagetype = args.messagetype
    else:
        parser.error("Both editype and messagetype, or a file path, are required.")

    botsinit.generalinit(args.config)  # find locating of bots, configfiles, init paths etc.
    process_name = "grammarcheck"
    botsglobal.logger = botsinit.initenginelogging(process_name)
    atexit.register(logging.shutdown)

    try:
        grammar.grammarread(editype, messagetype, typeofgrammarfile="grammars")
    except Exception as e:
        print(("Found error in grammar: ", botslib.txtexc()))
        sys.exit(1)
    else:
        print("OK - no error found in grammar")
        sys.exit(0)


if __name__ == "__main__":
    start()
