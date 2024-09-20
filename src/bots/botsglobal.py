# -*- coding: utf-8 -*-


try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

#Globals used by Bots
try:
    version = importlib_metadata.version('bots')  # bots version
except importlib_metadata.PackageNotFoundError:
    version = "unknown"  # Set a default version if 'bots' package is not found
db = None  # db-object
ini = None  # ini-file-object that is read (bots.ini)
logger = None  # logger or bots-engine
logmap = None  # logger for mapping in bots-engine
settings = None  # django's settings.py
usersysimportpath = None
currentrun = None  # needed for minta4query
routeid = ''  # current route. This is used to set routeid for Processes.
confirmrules = []  # confirmrules are read into memory at start of run
not_import = set()  # register modules that are not importable
