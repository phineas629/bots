#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

import pytest

import bots.botsglobal as botsglobal
import bots.botsinit as botsinit
import bots.botslib as botslib
from bots.botsconfig import *

"""
no plugin needed.
run in commandline.
should give no errors.
utf-16 etc are reported.
"""


def _testraise(expect_txt, *args, **kwargs):
    """Helper function to test raising BotsError with various parameters.
    Not a test function itself - used by actual test methods.
    """
    try:
        if not args and not kwargs:
            raise botslib.BotsError("")
        elif len(args) == 1 and not kwargs:
            raise botslib.BotsError(args[0])
        elif len(args) == 2 and not kwargs:
            raise botslib.BotsError(args[0], args[1])
        else:
            raise botslib.BotsError(*args, **kwargs)
    except botslib.BotsError as msg:
        # In Python 3, BotsError doesn't have a 'value' attribute
        # Get the error message either from .value (Python 2) or by converting to string (Python 3)
        error_value = getattr(msg, "value", str(msg))

        if expect_txt and error_value != expect_txt:
            print('Error,expect "%s" but got "%s"' % (expect_txt, error_value))
        if isinstance(error_value, str):
            pass
        else:
            print("Error,expect string but got %s" % type(error_value))


# .decode(): bytes->unicode
# .encode(): unicode -> bytes


class TestErrorCharsets(unittest.TestCase):
    def test_error_charsets(self):
        print("\n")
        # no parameters
        _testraise(
            "",
        )
        # one parameter; value
        _testraise("test")
        _testraise("test", "test")
        _testraise(
            "test",
            "test",
        )
        _testraise("test1 test2", "test1 %(test2)s", {"test2": "test2"})
        _testraise("test1 test2", "test1 %(test2)s", test2="test2")
        _testraise("test1 test2", "test1 %(test2)s", {"test2": "test2"})
        _testraise("test1 test2", "test1 %(test2)s", test2="test2")
        # one list
        _testraise("test1,test2", "test1,%(list)s", {"list": ["test2"]})
        _testraise("test1,test2", "test1,%(list)s", list=["test2"])
        # list of strings
        _testraise("test1,test2,test3", "test1,%(list)s", {"list": ["test2", "test3"]})
        _testraise("test1,test2,test3", "test1,%(list)s", list=["test2", "test3"])
        # formating of list
        _testraise("test1 test2 test3", "test1 %(list)s", {"list": [["test2", "test3"]]})
        _testraise("test1 test2 test3", "test1 %(list)s", list=[["test2", "test3"]])
        _testraise("test1 test2 test3", "test1 %(list)s", {"list": {"test2": "test3"}})
        _testraise("test1 test2 test3", "test1 %(list)s", list={"test2": "test3"})
        # list with more complicated formatter
        _testraise("test1 test2[test3]", "test1 %(l0)s[%(l1)s]", {"l0": "test2", "l1": "test3"})
        _testraise("test1 test2[test3]", "test1 %(l0)s[%(l1)s]", l0="test2", l1="test3")
        # errors
        _testraise(
            "4test test1 test2",
            "4test %(test1)s %(test2)s %(test3)s",
            {"test1": "test1", "test2": "test2"},
        )
        _testraise(
            "5test test1 test2", "5test %(test1)s %(test2)s %(test3)s", test1="test1", test2="test2"
        )
        _testraise("6test", "6test %(test1)s %(test2)s %(test3)s", "test1")
        _testraise(
            "7test ['test1', 'test2']",
            "7test %(test1)s %(test2)s %(test3)s",
            test1=["test1", "test2"],
        )
        _testraise(
            "8test {'test1': 'test1', 'test2': 'test2'}",
            "8test %(test1)s %(test2)s %(test3)s",
            test1={"test1": "test1", "test2": "test2"},
        )
        _testraise(
            "9test [<module 'bots.botslib' from '/home/hje/Bots/botsdev/bots/botslib.pyc'>, <module 'bots.botslib' from '/home/hje/Bots/botsdev/bots/botslib.pyc'>]",
            "9test %(test1)s %(test2)s %(test3)s",
            test1=[botslib, botslib],
        )

        # different charsets in BotsError
        _testraise(
            "12test test1 test2 test3",
            "12test %(test1)s %(test2)s %(test3)s",
            {"test1": "test1", "test2": "test2", "test3": "test3"},
        )
        _testraise(
            "13test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test2\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test3\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
            "13test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 %(test1)s %(test2)s %(test3)s",
            {
                "test1": "test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
                "test2": "test2\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
                "test3": "test3\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
            },
        )
        _testraise(
            "14test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
            "14test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 %(test1)s".encode(
                "utf_8"
            ),
            {
                "test1": "test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202".encode(
                    "utf_8"
                )
            },
        )
        _testraise("15test test1", "15test %(test1)s", {"test1": "test1".encode("utf_16")})
        _testraise(
            "16test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
            "16test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 %(test1)s",
            {
                "test1": "test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202".encode(
                    "utf_16"
                )
            },
        )
        _testraise(
            "17test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202",
            "17test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202 %(test1)s",
            {
                "test1": "test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC\\u0103\\u0178\\u01A1\\u0202".encode(
                    "utf_32"
                )
            },
        )
        _testraise(
            "18test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC",
            "18test\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC %(test1)s",
            {"test1": "test1\\u00E9\\u00EB\\u00FA\\u00FB\\u00FC".encode("latin_1")},
        )
        _testraise("19test test1", "19test %(test1)s", {"test1": "test1".encode("cp500")})
        _testraise("20test test1", "20test %(test1)s", {"test1": "test1".encode("euc_jp")})

        # Test with a limited range of Unicode characters to avoid surrogate issues
        l = []
        for i in range(0, 1000):  # Limit to a safe range
            l.append(chr(i))
        s = "".join(l)
        print(type(s))
        _testraise("", s)


# For backward compatibility
def testrun():
    test = TestErrorCharsets()
    test.test_error_charsets()


if __name__ == "__main__":
    botsinit.generalinit("config")
    botsinit.initbotscharsets()
    botsglobal.logger = botsinit.initenginelogging("engine")
    botsglobal.ini.set("settings", "debug", "False")
    testrun()
    botsglobal.ini.set("settings", "debug", "True")
    testrun()
