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

    # def _setpath(self)->Path:
    #     """_setpath()
    #     finds the .bat (for windows) or .sh (for linux) echo test files
    #     to allow use of the test programs on windows or linux

    #     Returns:
    #         Path: [description]
    #     """
    #     dbp:str = {'Linux':'testecho.sh', 'Windows':'testecho.bat', }.get(platform.system(),None)
    #     cwdp:Path = Path(os.getcwd())
    #     if 'tests' not in cwdp.parts:
    #         cwdp = cwdp / Path('tests')
    #     result:Path = cwdp / Path(dbp)
    #     _bbb = (result.exists() and 
    #                     result.is_file() and 
    #                     result.is_absolute()
    #                     )
    #     self.assertTrue(_bbb)
    #     if platform.system() == 'Windows':
    #         self.assertTrue(repr(result).startswith('WindowsPath'))
    #     elif platform.system() == 'Linux':
    #         self.assertTrue(repr(result).startswith('PosixPath'))
    #     else:
    #         self.assertTrue(False,'incorrect op sys / path type')
    #     return result

    @classmethod
    def setUpClass(cls):
        #a = 0
        pass

    @classmethod
    def tearDownClass(cls):
        #a = 1
        pass

    def test_01instant(self):
        """test_01instant
            check that the relay works
        """
        aa =sys.argv
        sys.argv = ['test.py','-h','fakename.json']
        try:
            ns: argparse.Namespace = loadprams.setup_parser()
            self.fail('-h did not cause exit')
        
        except (KeyboardInterrupt, SystemExit) as _:

            pass
        
        pass
    

    

if __name__ == '__main__':
    unittest.main()