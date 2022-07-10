#!/usr/bin/env python3.10
"""
Test file for tncmonitor
"""

from pathlib import Path
import unittest
import inspect
import os
import sys
from typing import (Any,  Dict, Tuple)
#import urllib3
import tncmonitor

ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)

# from tncmonitor import FindLogFile, Check4noInit, PsudoMain, internet_on, setup_parser, \
#     _send_end_email, _send_start_email, INResponse


JAT = 'just a test...ignore'
JUNK_com = "junk.r@gmail.com"


def execution_path(filename: str) -> Path:
    """p:Path = execution_path(filename)

    see: https://docs.python.org/3/library/sys.html for documentation on _getframe

    Args:
        filename (str): _description_

    Returns:
        Path: _description_
    """  # ! TODO you do not know what this is for or what it does
    result: Path = Path(os.path.dirname(
        inspect.getfile(sys._getframe(1)))) / filename
    return result


class TestTncmonitor(unittest.TestCase):
    """

    """

    def setUp(self):
        #b = 0
        pass

    def tearDown(self):
        #b = 1
        pass

    @classmethod
    def setUpClass(cls):
        cls.a = 0

    @classmethod
    def tearDownClass(cls):
        cls.a = 1

    def test_01internet_on(self):
        """

        """
        #from tncmonitor import internet_on, INResponse
        jj: tncmonitor.INResponse = tncmonitor.internet_on()
        self.assertTrue(jj.ok, 'internet not on')

    def test_02setTimers(self):
        """

        """
        # s = self
        pt: Path = execution_path('testLogData')
        pm = tncmonitor.PsudoMain({
            'rmslogdir': str(pt),
            'moduleid': '1234a',
            'age': 0,
            'program': './tests/testecho.bat',
            'relay': '01',
            'powerofftime': 1,
            'emsub': JAT,
            "account": "junk",
            "password": "password",
            "fromemail": JUNK_com,
            "toemail": [
                "junk@gmail.com",
                "junk@outlook.com",
                JUNK_com,
            ],
            'emailonly': True,
            'testing': True,

        })

        jj: Tuple[int, ...] = pm.set_timers(None)
        self.assertEqual(jj, (0,))
        jj = pm.set_timers((1,))
        self.assertEqual(jj, (1,))
        jj = pm.set_timers((1, 2, 3, 4, 5,))
        self.assertEqual(jj, (1, 2, 3, 4, 5,))

    def test_05PsudoMain(self):
        """
            tests that the check3noinit and findlogfile code is working correctly,
            email is disabled because testing is true and prams['emacnt'] is None
        """

        s = self
        pt: Path = execution_path('testLogData')
        pm = tncmonitor.PsudoMain({
            'rmslogdir': str(pt),
            'moduleid': '1234a',
            'age': 0,
            'program': './tests/testecho.bat',
            'relay': '01',
            'powerofftime': 1,
            'emsub': JAT,
            "account": "junk",
            "password": "password",
            "fromemail": JUNK_com,
            "toemail": [
                "junk@gmail.com",
                "junk@outlook.com",
                JUNK_com,
            ],
            'emailonly': True,
            'testing': True,

        })

        pm.doit(timersin=(1, 1), count=1)
        if pm.c4ni is not None and pm.c4ni.filepath is not None and pm.c4ni.detectedline is not None:

            s.assertTrue('20180615' in pm.c4ni.filepath.name)
            s.assertTrue('DISCONNECTED' in pm.c4ni.detectedline)

            pm.doit(timersin=(1, 1), count=1, age1=2)
            s.assertTrue('20180613' in pm.c4ni.filepath.name)
            s.assertTrue('initialization failed' in pm.c4ni.detectedline)

    def test_07AAA(self):
        import loadprams

        pt: Path = execution_path('testLogData')
        pm = tncmonitor.PsudoMain({
            'rmslogdir': str(pt),
            'moduleid': '1234a',
            'age': 0,
            'program': './tests/testecho.bat',
            'relay': '01',
            'powerofftime': 1,
            'emsub': JAT,
            "fromemail":  JUNK_com,
            "toemail": [
                "junk@gmail.com",
                "junk@outlook.com",
                JUNK_com,
            ],
            'emailonly': True,
            'testing': True,
            'testingaccount': 'junk',
            'password': 'password'
        })
        yamlpth: Path = execution_path('testtncprams.yaml')

        pramdict: Dict[str, Any] = loadprams.setup_basic_prams(yamlpth)

        from myemail import MyEmail
        acnt: MyEmail.Accntarg = MyEmail.Accntarg(
            accountid=pramdict['account'],
            password=pramdict['password'],
            url=pramdict['SMTPServer'])
        pm.prams['emacnt'] = acnt
        aa = None
        aa = pm.send_email(True)
        self.assertTrue(aa)
        aa = pm.send_email(False)
        self.assertEqual(1, len(aa))
        cc = aa.get('sentem')
        if cc is not None:
            self.assertTrue(JAT in cc)


if __name__ == '__main__':
    unittest.main()
