#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Add future imports for Python 2/3 compatibility
from __future__ import print_function, division, absolute_import

import sys
import os
import codecs
import logging
import logging.handlers
import datetime

# Use six for Python 2/3 compatibility
try:
    import six
except ImportError:
    # Handle case where six is not installed
    pass

try:
    import configparser
except ImportError:
    import ConfigParser as configparser  # for Python 2.7

from . import botsglobal
from . import botslib

# **********************************************************************************


class BotsConfig(configparser.RawConfigParser):
    """Class for configuration. Does the botsconfig file.
    Implemented as singleton. Values are accessed as attributes.
    There is a hack: if you get config.set('section','option',value), this will change the return value
    for config.get config.get('section','option') !! (needed for reading config in  usersys)"""

    def get(self, section, option, default="", **kwargs):
        if kwargs:
            if not botsglobal.ini:
                return default
            return botsglobal.ini.get(section, option, **kwargs)
            # the hack
            # return value = kwargs.get('defaultvalue')
        try:
            return super(BotsConfig, self).get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, TypeError):
            return default

    def getint(self, section, option, default, **kwargs):
        if not botsglobal.ini:
            return default
        try:
            return super(BotsConfig, self).getint(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, TypeError):
            return default

    def getboolean(self, section, option, default, **kwargs):
        if not botsglobal.ini:
            return default
        try:
            return super(BotsConfig, self).getboolean(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError, TypeError):
            return default


# **********************************************************************************
def generalinit(configdir):
    ##########################################################################
    # Configdir: settings.py & bots.ini#########################################
    # Configdir MUST be importable. So configdir is relative to PYTHONPATH. Try several options for this import.
    configsetting = {}
    configmodule = None
    
    # Instead of using exec, use importlib to dynamically import modules
    import importlib
    
    # Try different import approaches
    importnameforsettings = ".".join((configdir, "settings"))
    try:  # first try a relative import path
        configmodule = importlib.import_module(importnameforsettings)
    except ImportError:
        pass
        
    if not configmodule:
        try:  # try another method for relative import (used by python egg installations)
            configmodule = importlib.import_module("{}.settings".format(configdir))
        except ImportError:
            pass
            
    if not configmodule:
        try:
            configmodule = importlib.import_module("settings")  # default, settings.py is in PYTHONPATH
        except ImportError:
            pass
            
    if not configmodule:
        from bots import botsglobal
        raise botsglobal.BotsImportError(
            "In initilisation: Could not import configuration. Tried import settings, import %s.settings,"
            "import %s, tried import settings, absolutly and relative." % (configdir, configdir)
        )

    # Get configuration values from settings.py
    importedfromsettings = ["BOTS_INI", "LOCALECONF", "BOTSPASSWORD"]
    configsetting = {key: getattr(configmodule, key) for key in importedfromsettings if hasattr(configmodule, key)}

    # Get path to configuration file
    botsglobal.ini = BotsConfig()
    botsglobal.ini.config_file = (
        configsetting.get("BOTS_INI") if "BOTS_INI" in configsetting else "bots/config/bots.ini"
    )

    # Read configuration file
    try:
        botsglobal.ini.read(botsglobal.ini.config_file)
    except Exception as msg:
        raise botsglobal.BotsImportError(
            "In initilisation: Could not read ini file: {}; exception: {}".format(botsglobal.ini.config_file, msg)
        )

    # Get configuration from other modules
    botssys = botsglobal.ini.get("directories", "botssys", "botssys")
    botsglobal.usersysimportdir = botsglobal.ini.get("directories", "usersysimportpath", "usersys")
    botsglobal.usersys = botssys
    botsglobal.ini.set(
        "directories",
        "botssys",
        botssys,
    )  # the hack
    
    # Import settings - use importlib instead of exec
    import importlib
    import sys
    
    # Try to import from configdir.settings
    try:
        importnameforsettings = ".".join((configdir, "settings"))
        settings_module = importlib.import_module(importnameforsettings)
        # Import all attributes from settings_module to global namespace
        globals().update({name: getattr(settings_module, name) for name in dir(settings_module) 
                         if not name.startswith('_')})
    except (ImportError, AttributeError):
        pass
        
    # If settings already in sys.modules but usersys isn't, import from settings
    if "settings" in sys.modules and "usersys" not in sys.modules:
        try:
            settings_module = importlib.import_module("settings")
            # Import all attributes from settings_module to global namespace
            globals().update({name: getattr(settings_module, name) for name in dir(settings_module)
                             if not name.startswith('_')})
        except (ImportError, AttributeError):
            pass

    # Set environment settings
    botsglobal.confirmdirectory = botsglobal.ini.get("directories", "confirm_directory", "botssys/confirmdirectory")
    expand_envvars = botsglobal.ini.getboolean(
        "acceptance", "expand_envvars", False
    )  # Expand environment variables in paths
    if expand_envvars:
        botsglobal.ini.config_file = os.path.expandvars(botsglobal.ini.config_file)
        botsglobal.confirmdirectory = os.path.expandvars(botsglobal.confirmdirectory)
        botssys = os.path.expandvars(botssys)
        botsglobal.usersys = os.path.expandvars(botsglobal.usersys)

    # Make abspaths and set dirs
    directory_botssys = botslib.join(botssys)
    botsglobal.confirmdirectory = botslib.join(botsglobal.confirmdirectory)
    for key in [
        "config_directory",
        "data_directory",
        "logging_directory",
        "temp_directory",
        "archive_directory",
    ]:
        value = botsglobal.ini.get("directories", key, "botssys/subdirectory_not_defined")
        if expand_envvars:
            value = os.path.expandvars(value)
        value = botslib.join(value)
        botsglobal.ini.set("directories", key, value)  # *************the hack here!!
        botslib.dirshouldbethere(value, key)

    # Get database settings
    botsglobal.settings = {}  # Init settings dict if not already present
    for section in ["database", "settings", "directories", "acceptance"]:
        if botsglobal.ini.has_section(section):
            for key, value in botsglobal.ini.items(section):
                if section == "directories" and expand_envvars and value:
                    value = os.path.expandvars(value)
                # convert types int
                if value.isdigit():
                    value = int(value)
                # convert types bool
                if value == "False":
                    value = False
                if value == "True":
                    value = True
                botsglobal.settings[key] = value


# **********************************************************************************


def initbotscharsets():
    """set up right charset handling and check if charset mappings are correct."""
    codecs.register(codec_search_function)  # register the special bots codec.ascii_botscodec
    # Use six.text_type for unicode compatibility
    try:
        botsglobal.botsreplacechar = six.text_type(botsglobal.ini.get("settings", "botsreplacechar", " "))
    except NameError:
        # Fallback if six is not available
        try:
            botsglobal.botsreplacechar = unicode(botsglobal.ini.get("settings", "botsreplacechar", " "))
        except NameError:
            # For Python 3
            botsglobal.botsreplacechar = str(botsglobal.ini.get("settings", "botsreplacechar", " "))


def codec_search_function(encoding):
    """for the special bots encodings, this function is called by Python."""
    if not hasattr(botsglobal, 'all_encodings'):
        botsglobal.all_encodings = ["ascii_botscodec", "ascii_strict"]
    if encoding not in botsglobal.all_encodings:
        return None
    if encoding in ("ascii_botscodec", "ascii_strict"):  # bots default strict handlings of ascii
        return (codec_for_strict_ascii, None)
    return (codec_for_other_encodings, None)


def codec_for_strict_ascii(input, errors="strict"):
    """vencode according to bots rules.
    1. if errors='strict': really strict handling
    2. if errors='bots': replace character, give warning
    in both cases: if character>128, does not fit in byte...
    Bots is pretty strict for encoding; files should be unicode inside bots,
    so encoding has to work.
    Reason: in order to make predictable translations
    """
    try:
        return codecs.ascii_encode(input, "strict")
    except UnicodeError:
        if errors == "strict":
            raise
        warnings = []
        result = []
        for c in input:
            try:
                b = codecs.ascii_encode(c, "strict")
            except UnicodeError:
                b = botsglobal.botsreplacechar
                warnings.append("Changed character '{}' (non-ascii).".format(c))
            result.append(b[0])
        from . import botslib

        botslib.sendbotserrorreport("ascii-encoding", warnings)
        # Use proper string joining for Python 2/3 compatibility
        return ("".join(result).encode("ascii"), len(input))


def codec_for_other_encodings(input, errors="strict"):
    """handle e.g. encoding cp500, latin1, etc.
    I use None for the standard handling in case of errors
    """
    return None


def botsreplacechar_handler(info):
    """special handler for botsreplacechar. Like strict_handler, but replaces 'errors' with botsreplacechar.
    input: unicode
    output : same unicode
    """
    result = []
    warnings = []
    for c in info.object[info.start : info.end]:
        result.append(botsglobal.botsreplacechar)
        warnings.append("Changed character '{}' to {} (not in encoding).".format(c, botsglobal.botsreplacechar))
    from . import botslib

    botslib.sendbotserrorreport(info.encoding, warnings)
    return ("").join(result)


# **********************************************************************************


def connect():
    """connect to database for non-django modules eg engine"""
    if botsglobal.settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3":
        # sqlite has some more fiddling; in separate file. Mainly because of some other method of parameter passing.
        db_path = botsglobal.settings.DATABASES["default"]["NAME"]
        db_dir = os.path.dirname(db_path)
        # Create directory if it doesn't exist
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        # For SQLite, we can create the database file if it doesn't exist
        from . import botssqlite

        botsglobal.db = botssqlite.connect(database=db_path)
    elif botsglobal.settings.DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
        import MySQLdb
        from MySQLdb import cursors

        # Handle OPTIONS dict for Python 2 compatibility
        options_dict = {}
        if "OPTIONS" in botsglobal.settings.DATABASES["default"]:
            options_dict = botsglobal.settings.DATABASES["default"]["OPTIONS"]
        
        botsglobal.db = MySQLdb.connect(
            host=botsglobal.settings.DATABASES["default"]["HOST"],
            port=int(botsglobal.settings.DATABASES["default"]["PORT"]),
            db=botsglobal.settings.DATABASES["default"]["NAME"],
            user=botsglobal.settings.DATABASES["default"]["USER"],
            passwd=botsglobal.settings.DATABASES["default"]["PASSWORD"],
            cursorclass=cursors.DictCursor,
            **options_dict
        )
    elif (
        botsglobal.settings.DATABASES["default"]["ENGINE"]
        == "django.db.backends.postgresql_psycopg2"
    ):
        import psycopg2
        import psycopg2.extensions
        import psycopg2.extras

        psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        botsglobal.db = psycopg2.connect(
            host=botsglobal.settings.DATABASES["default"]["HOST"],
            port=botsglobal.settings.DATABASES["default"]["PORT"],
            database=botsglobal.settings.DATABASES["default"]["NAME"],
            user=botsglobal.settings.DATABASES["default"]["USER"],
            password=botsglobal.settings.DATABASES["default"]["PASSWORD"],
            connection_factory=psycopg2.extras.DictConnection,
        )
        botsglobal.db.set_client_encoding("UNICODE")
    else:
        raise botslib.PanicError(
            'Unknown database engine "%(engine)s".',
            {"engine": botsglobal.settings.DATABASES["default"]["ENGINE"]},
        )
