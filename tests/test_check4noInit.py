#!/usr/bin/env python3
"""
Test file for check4noInit.py
"""
import os
import sys
from typing import List, Any, Dict, Tuple
import platform
from time import sleep
import subprocess
from subprocess import CompletedProcess
import inspect
import unittest
from pathlib import Path
import copy

ppath=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)
from check4noInit import Check4noInit
from findlogfile import FindLogFile


class TestCheck4noInit(unittest.TestCase):
    """"""
    BAD_CONFIG:bool=False
    TEST_DIR:Path=None
    
    def setUp(self):
        self.assertFalse(TestCheck4noInit.BAD_CONFIG)      
        self.logpath:Path = TestCheck4noInit.TEST_DIR / 'testLogData'
        self.assertTrue(self.logpath.exists() and self.logpath.is_dir())


    def tearDown(self):
        #b = 1
        pass

    @classmethod
    def setUpClass(cls):
        
        lastpart = Path.cwd().parts[-1]
        
        if  lastpart !='tests' or lastpart != 'tncmonitor':
            if lastpart=='tncmonitor':
                cls.TEST_DIR=Path.cwd() / 'tests'
            else:
                cls.TEST_DIR=Path.cwd()
        else:
            print('Fail not on .../tncmonitor/tests/')
            cls.BAD_CONFIG=True
        

    @classmethod
    def tearDownClass(cls):
        pass

    def test_01instant(self):
        """test_01instant
            check instantiation and str() and repr()
        """
        mtdict:Dict[str,str]= {'testing':True}
        c4n:Check4noInit = Check4noInit(mtdict,self.logpath)
        estr:str = 'path: None, dline: None'
        erepr:str = "<class 'check4noInit.Check4noInit'>({'prams': {'testing': True}, 'dirpath': WindowsPath('m:/Python/Python3_packages/tncmonitor/tests/testLogData'), 'filepath': None, 'detectedline': None})"

        self.assertEqual(estr, str(c4n))
        self.assertEqual(erepr, repr(c4n))
        pass
        

    
    def test_03Check4noInit(self):
        """
        checks to detect erroring lines in the log

        """
        s = self
        pt: Path = self.logpath
        
        ## check for text path and result from age none
        c4ni: Check4noInit = Check4noInit({'rmslogdir': str(pt)})
        result: Check4noInit.Result = c4ni.doit()
        s.assertEqual((False, True), result[0:2])
        s.assertFalse(result.result)
        s.assertTrue(result.status)
        s.assertTrue('20180615' in c4ni.filepath.name)
        s.assertTrue('DISCONNECTED' in c4ni.detectedline)
        s.assertTrue('DISCONNECTED' in result.dl)

        ## check for text path and result from age 0 (same as none)
        result = c4ni.doit(0)
        s.assertEqual((False, True), result[0:2])
        s.assertTrue('20180615' in c4ni.filepath.name)
        s.assertTrue('DISCONNECTED' in result.dl)
        
        ## check for text path and result from age 1
        result = c4ni.doit(1)
        s.assertEqual((False, True), result[0:2])
        s.assertFalse(result.result)
        s.assertTrue(result.status)
        s.assertTrue('20180614' in c4ni.filepath.name)
        s.assertTrue('DISCONNECTED' in result.dl)

        result = c4ni.doit(2)
        s.assertEqual((True, True), result[0:2])
        s.assertTrue('20180613' in c4ni.filepath.name)
        s.assertTrue('initialization failed' in result.dl)
        
        ## check for path not leading to log directory
        c4ni = Check4noInit({'rmslogdir': Path.cwd()})
        result = c4ni.doit()
        s.assertTrue((True, False, None), result)
        s.assertFalse(c4ni.filepath)
        s.assertFalse(c4ni.detectedline)


if __name__ == '__main__':
    unittest.main()

