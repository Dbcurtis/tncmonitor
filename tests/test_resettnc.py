#!/usr/bin/env python3
"""
Test file for tncmonitor
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

ppath=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)
from resettnc import ResetTNC

class TestResettnc(unittest.TestCase):
    """"""

    def setUp(self):
        #b = 0
        pass

    def tearDown(self):
        #b = 1
        pass

    def _setpath(self)->Path:
        dbp:str = {'Linux':'testecho.sh', 'Windows':'testecho.bat', }.get(platform.system(),None)
        cwdp:Path = Path(os.getcwd())
        if 'tests' not in cwdp.parts:
            cwdp = cwdp / Path('tests')
        result:Path = cwdp / Path(dbp)
        _bbb = (result.exists() and 
                        result.is_file() and 
                        result.is_absolute()
                        )
        self.assertTrue(_bbb)
        if platform.system() == 'Windows':
            self.assertTrue(repr(result).startswith('WindowsPath'))
        elif platform.system() == 'Linux':
            self.assertTrue(repr(result).startswith('PosixPath'))
        else:
            self.assertTrue(False,'incorrect op sys / path type')
        return result

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
        argdic = {
            'moduleid': '3D0V2',
            'relay': '01',
            "program": "CommandApp_USBRelay",
            "powerofftime": 5,
        }
        expectedlist:List[str]=['CommandApp_USBRelay', '3D0V2', 'close', '01']
        resettnc:ResetTNC = ResetTNC(argdic)
        
        self.assertEqual(expectedlist,resettnc.cpi.args)
        self.assertEqual(0,resettnc.cpi.returncode)
        self.assertFalse(resettnc.cpi.stderr)
        self.assertFalse(resettnc.cpi.stdout)
        self.assertEqual('PU',resettnc.state)
        expstr = "TNC prams:{'moduleid': '3D0V2', 'relay': '01', 'program': 'CommandApp_USBRelay', 'powerofftime': 5}, state: PU"
        self.assertEqual(expstr,str(resettnc))

        resettnc.doit()
        tups:List[Tuple[str, ...]] = list(resettnc.history)
        self.assertEqual(3,len(tups))
        self.assertEqual('PU',tups[0][1])
        self.assertEqual('PU',tups[2][1])
        self.assertEqual('PD',tups[1][1])


    def test_00subprocess(self):
        """test_00subprocess
            checks that I can call subprocesses
        """
        print('need to check this on a unix system')
        #dbp:str = {'Linux':'testecho.sh', 'Windows':'testecho.bat', }.get(platform.system(),None)
        
        CPI_TEST:CompletedProcess = subprocess.run(['python', '--version'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )
        #cpitest = str(CPI_TEST)
        self.assertEqual("['python', '--version']", str(CPI_TEST.args))
        self.assertEqual(0, CPI_TEST.returncode)
        self.assertTrue('Python ' in str(CPI_TEST.stdout))
        
        CPI_TEST:CompletedProcess = subprocess.run(['echo','one two three'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )
        #cpitest = str(CPI_TEST)
        self.assertEqual("['echo', 'one two three']", str(CPI_TEST.args))
        self.assertEqual(0, CPI_TEST.returncode)
        self.assertTrue('one two three' in str(CPI_TEST.stdout))

        batpath:Path = self._setpath()

        CPI_TEST:CompletedProcess = subprocess.run([batpath, 'one', 'two'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )

        
        if platform.system() == 'Windows': 
            self.assertTrue(repr(CPI_TEST.args[0]).startswith('WindowsPath'))
            self.assertEqual('one',CPI_TEST.args[1])
            self.assertEqual('two',CPI_TEST.args[2])
            self.assertEqual(0, CPI_TEST.returncode)
            self.assertTrue('test one two' in CPI_TEST.stdout)
        else:
            self.assertTrue((CPI_TEST.args[0]).startswith('PosixPath'))
            self.assertEqual('one',CPI_TEST.args[1])
            self.assertEqual('two',CPI_TEST.args[2])
            self.assertEqual(0, CPI_TEST.returncode)
            self.assertTrue('test one two' in str(CPI_TEST.stdout))



if __name__ == '__main__':
    unittest.main()

