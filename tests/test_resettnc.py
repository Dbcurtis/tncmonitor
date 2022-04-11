#!/usr/bin/env python3.10
"""
Test file for tncmonitor

You will need to set the argdic values in test_01...

"""
from resettnc import ResetTNC
import os
import sys
from typing import (List, Dict, Tuple,)
import platform

import subprocess


import unittest
from pathlib import Path

ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)


class TestResettnc(unittest.TestCase):
    """"""

    def setUp(self):
        #b = 0
        pass

    def tearDown(self):
        #b = 1
        pass

    def _setpath(self) -> Path:
        """_setpath()
        finds the .bat (for windows) or .sh (for linux) echo test files
        to allow use of the test programs on windows or linux

        Returns:
            Path: [description]
        """
        dbp: str = {'Linux': 'testecho.sh', 'Windows': 'testecho.bat', }.get(
            platform.system(), None)
        cwdp: Path = Path(os.getcwd())
        if 'tests' not in cwdp.parts:
            cwdp = cwdp / Path('tests')
        result: Path = cwdp / Path(dbp)
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
            self.assertTrue(False, 'incorrect op sys / path type')
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
        #! TODO setup the argdic values to your configuration
        argdic: Dict[str, str] = {
            'moduleid': '3D0V2',
            'relay': '01',
            "program": "CommandApp_USBRelay",
            "powerofftime": '5.0'
        }
        expectedlist: List[str] = [
            'CommandApp_USBRelay', '3D0V2', 'close', '01']

        resettnc = ResetTNC(argdic)

        self.assertEqual(expectedlist, resettnc.cpi.args)
        self.assertEqual(0, resettnc.cpi.returncode)
        self.assertFalse(resettnc.cpi.stderr)
        self.assertFalse(resettnc.cpi.stdout)
        self.assertEqual('PU', resettnc.state)
        expstr = "TNC prams:{'moduleid': '3D0V2', 'relay': '01', 'program': 'CommandApp_USBRelay', 'powerofftime': '5.0'}, state: PU"
        self.assertEqual(expstr, str(resettnc))

        resettnc.doit()
        tups: List[Tuple[str, ...]] = list(resettnc.history)
        self.assertEqual(3, len(tups))
        self.assertEqual('PU', tups[0][1])
        self.assertEqual('PU', tups[2][1])
        self.assertEqual('PD', tups[1][1])

    def test_00subprocess(self):
        """test_00subprocess
            check that I can call subprocesses on windows and linux
        """
        print('need to check this on a unix system')
        #dbp:str = {'Linux':'testecho.sh', 'Windows':'testecho.bat', }.get(platform.system(),None)

        cpi_test = subprocess.run(['python', '--version'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=False,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )
        #cpitest = str(CPI_TEST)
        self.assertEqual("['python', '--version']", str(cpi_test.args))
        self.assertEqual(0, cpi_test.returncode)
        self.assertTrue('Python ' in str(cpi_test.stdout))

        cpi_test = subprocess.run(['echo', 'one two three'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )

        self.assertEqual("['echo', 'one two three']", str(cpi_test.args))
        self.assertEqual(0, cpi_test.returncode)
        self.assertTrue('one two three' in str(cpi_test.stdout))

        batpath: Path = self._setpath()

        cpi_test = subprocess.run([batpath, 'one', 'two'],  # tests ability to run a subprocess.
                                  input=None,
                                  timeout=1,
                                  check=False,
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  encoding='ascii',
                                  )

        if platform.system() == 'Windows':
            self.assertTrue(repr(cpi_test.args[0]).startswith('WindowsPath'))
            self.assertEqual('one', cpi_test.args[1])
            self.assertEqual('two', cpi_test.args[2])
            self.assertEqual(0, cpi_test.returncode)
            self.assertTrue('test one two' in cpi_test.stdout)
        else:
            self.assertTrue((cpi_test.args[0]).startswith('PosixPath'))
            self.assertEqual('one', cpi_test.args[1])
            self.assertEqual('two', cpi_test.args[2])
            self.assertEqual(0, cpi_test.returncode)
            self.assertTrue('test one two' in str(cpi_test.stdout))


if __name__ == '__main__':
    unittest.main()
