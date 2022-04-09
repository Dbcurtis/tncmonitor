#!/usr/bin/env python3.10
"""
Test file for findlogfile
"""
import os
import sys
from typing import (List, Any, Dict, Tuple,)
import platform
#from time import sleep
#import subprocess
#from subprocess import CompletedProcess
#import inspect
import unittest
from pathlib import Path

ppath=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)
from findlogfile import FindLogFile

class TestFindlogfile(unittest.TestCase):
    """"""

    def setUp(self):
        #b = 0BB
        pass

    def tearDown(self):
        #b = 1
        pass
    
    def setdir(self):
        cwd:Path = Path.cwd()
        if cwd.parts[-1]!= 'tests':
            cwd = cwd / 'tests'
        dip:Path = cwd / 'testLogData'
        return dip


    @classmethod
    def setUpClass(cls):
        cls.system:str = platform.system()
        
        pass

    @classmethod
    def tearDownClass(cls):
        #a = 1
        pass

    def test_01instant(self):
        """test_01instant
            check that FindLogFile instantiates
        """
        
        # cwd:Path = Path.cwd()
        # if cwd.parts[-1]!= 'tests':
        #     cwd = cwd / 'tests'
            
        # dip:Path = cwd / 'testLogData'
        dip:Path = self.setdir()
        flf:FindLogFile = FindLogFile({},dip)
        if (TestFindlogfile.system == 'Windows'):
            
            sresult:str = ''.join(
                [
                    'm:\\Python\\Python3_packages\\tncmonitor\\',
                    'tests\\testLogData'
                    ])
    
            rresult:str = ''.join(
                [     
                    "<class 'findlogfile.FindLogFile'>({'prams': {}, 'dirpath': ",
                    "WindowsPath('m:/Python/Python3_packages/tncmonitor/tests/testLogData')})",
                    ])
            
            self.assertEqual(sresult, str(flf))
            self.assertEqual(rresult, repr(flf))
        if (TestFindlogfile.system == 'Linux'):
            #! TODO make this test for Linux
            self.fail("unimplemented code")
            pass
        
    def test_05doit(self):
        """test_05doit()
        
        """
        
        dip:Path = self.setdir()
        flf:FindLogFile = FindLogFile({},dip)
        result:Path|None = flf.doit(-1)
        self.assertTrue(result is None)
        result = flf.doit(1000)
        self.assertTrue(result is None)
        result = flf.doit(8)
        self.assertTrue(result is None)
        
        result0:Path|None = flf.doit(0)
        resultn:Path|None = flf.doit(None)
        resultnt:Path|None = flf.doit('0')
        self.assertEqual(result0, resultn)    
        self.assertEqual(result0, resultnt)   
        self.assertTrue('20180615.log' in str(result0))
        self.assertTrue('RMS Packet TNC Events' in str(result0))
        result1:Path|None = flf.doit(1)
        result7:Path|None = flf.doit(7)
        self.assertTrue('20180614.log' in str(result1))
        self.assertTrue('20180608.log' in str(result7))
        

if __name__ == '__main__':
    unittest.main()

