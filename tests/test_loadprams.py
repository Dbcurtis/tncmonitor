#!/usr/bin/env python3
"""
Test file for loadprams



"""
import os
import sys
from typing import List, Any, Dict, Tuple
import platform
from time import sleep
import subprocess
import argparse
from subprocess import CompletedProcess
import inspect
import unittest
from pathlib import Path

ppath=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)

import loadprams

class Testloadprams(unittest.TestCase):
    """"""

    def setUp(self):
        #b = 0
        pass

    def tearDown(self):
        #b = 1
        pass



    @classmethod
    def setUpClass(cls):
        #a = 0
        pass

    @classmethod
    def tearDownClass(cls):
        #a = 1
        pass

    def test_01loadpramsHelp(self):
        """test_01instant
            check that the relay works
        """
        aa = sys.argv
        aa = ['-h','fakename.yaml']
        try:
            ns: argparse.Namespace = loadprams.setup_parser(aa)
            self.fail('-h did not cause exit')
        
        except (KeyboardInterrupt, SystemExit) as _:
            pass
        
    
    def test_02loadpramsAll(self):
        """[summary]
        """
        aa = [ '-li', '-ld', '-eo', '-ese', '-t', 'pramfile']
        try:
            ns: argparse.Namespace = loadprams.setup_parser(aa)
            self.assertTrue(ns.emailonly)
            self.assertTrue(ns.emstartend)
            self.assertTrue(ns.logdebug)
            self.assertTrue(ns.loginfo)
            self.assertTrue(ns.testdata)
            self.assertEqual('pramfile',ns.pramfile)
        
        except (KeyboardInterrupt, SystemExit) as _:
            self.fail('caused exit')
            pass
        
    
    def test_03get_prams(self):
        """[summary]
        """        
        aa = ['-ld', '-eo', '-t', 'testtncprams.json']
        ns: argparse.Namespace = loadprams.setup_parser(aa)
        prams:Dict[str,Any]=loadprams.get_prams(ns)
        self.assertTrue(len(prams)>18)
        self.assertTrue(isinstance(prams['account'],str))
        self.assertTrue(isinstance(prams['age'],int))
        self.assertTrue(isinstance(prams['timers'],list))
        self.assertEqual(2,len(prams['timers']))
        
    

if __name__ == '__main__':
    unittest.main()