# -*- coding: utf-8 -*-

# Add future imports for Python 2/3 compatibility
from __future__ import print_function, division, absolute_import

# Import six for Python 2/3 compatibility
try:
    import six
except ImportError:
    # Define a minimal compatibility layer
    import sys
    
    class _Six(object):
        PY2 = sys.version_info[0] == 2
        PY3 = sys.version_info[0] == 3
        
        def iteritems(self, d):
            if self.PY2:
                return d.iteritems()
            else:
                return d.items()
    
    six = _Six()

# Handle importlib.metadata for package version detection
try:
    import importlib.metadata as importlib_metadata
except ImportError:
    try:
        import importlib_metadata
    except ImportError:
        importlib_metadata = None

# Custom exceptions for Bots
class BotsImportError(ImportError):
    """Exception raised for errors in the Bots import process."""
    pass

# Globals used by Bots
try:
    if importlib_metadata:
        version = importlib_metadata.version("bots")  # bots version
    else:
        version = "unknown"
except Exception:
    version = "unknown"  # Set a default version if 'bots' package is not found

db = None  # db-object
ini = None  # ini-file-object that is read (bots.ini)
logger = None  # logger or bots-engine
logmap = None  # logger for mapping in bots-engine
settings = None  # django's settings.py
usersysimportpath = None
currentrun = None  # needed for minta4query
routeid = ""  # current route. This is used to set routeid for Processes.
confirmrules = []  # confirmrules are read into memory at start of run
not_import = set()  # register modules that are not importable
