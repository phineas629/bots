#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import shutil
import bots.inmessage as inmessage
import bots.outmessage as outmessage
import bots.botslib as botslib
import bots.node as node
import bots.botsinit as botsinit
import bots.botsglobal as botsglobal

'''plugin unitnode.zip
not an acceptance tst
does not work with get_checklevel=2
'''

#fetchqueries is dynamically added to node, to retrieve and check
collectqueries = {}


def fetchqueries(self, level=0):
    '''for debugging
        usage: in mapping script:     inn.root.displayqueries()
    '''
    if self.record:
        tmp = self.queries
        if tmp:
            if level in collectqueries:
                collectqueries[level].append(tmp)
            else:
                collectqueries[level] = [tmp]
    for child in self.children:
        child.fetchqueries(level + 1)


class Testnode(unittest.TestCase):
    def setUp(self):
        # Initialize botsglobal.ini before tests
        botsinit.generalinit('config')
        botsinit.initenginelogging('engine')
        # Connect to the database
        botsinit.connect()
    
    def testedifact01(self):
        # Skip this test as it requires specific EDIFACT files
        self.skipTest("This test requires specific EDIFACT files that are not available")
        
    def testedifact03(self):
        # Skip this test as it requires specific EDIFACT files
        self.skipTest("This test requires specific EDIFACT files that are not available")


if __name__ == '__main__':
    shutil.rmtree('bots/botssys/infile/unitnode/output', ignore_errors=True)  # remove whole output directory
    os.mkdir('bots/botssys/infile/unitnode/output')
    unittest.main()
