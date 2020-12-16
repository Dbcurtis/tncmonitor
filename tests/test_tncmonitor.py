#!/usr/bin/env python3
"""
Test file for tncmonitor
"""

from pathlib import Path
import unittest
import inspect
import os
import sys
from typing import Any, List, Dict

ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)
from tncmonitor import FindLogFile, Check4noInit, PsudoMain, internet_on, setup_parser, \
    _send_end_email, _send_start_email, INResponse

def execution_path(filename) -> Path: #! TODO you do not know what this is for or what it does
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
        pass

    @classmethod
    def tearDownClass(cls):
        cls.a = 1
        pass

    def test_01internet_on(self):
        """

        """
        jj: INResponse = internet_on()
        self.assertTrue(jj.ok, 'internet not on')

    def test_05PsudoMain(self):
        """
            tests that the check3noinit and findlogfile code is working correctly,
            email is disabled because testing is true and prams['emacnt'] is None
        """
        s = self
        pt: Path = execution_path('testLogData')
        pm = PsudoMain({'rmslogdir': str(pt), 'moduleid': '1234a', 'age': 0, 'program': './tests/testecho.bat',
                        'relay': '01', 'powerofftime': 1, 'emsub': 'just a test...ignore',
                        "account": "junk",
                        "password": "password",
                        "fromemail": "junk.r@gmail.com",
                        "toemail": [
                            "junk@gmail.com",
                            "junk@outlook.com",
                            "junk.r@gmail.com"
                        ],
                        'emailonly': True,
                        'testing': True,

        })

        pm.doit(timers=(1, 1), count=1)
        s.assertTrue('20180615' in pm.c4ni.filepath.name)
        s.assertTrue('DISCONNECTED' in pm.c4ni.detectedline)

        pm.doit(timers=(1, 1), count=1, age1=2)
        s.assertTrue('20180613' in pm.c4ni.filepath.name)
        s.assertTrue('initialization failed' in pm.c4ni.detectedline)
        
    def test_07AAA(self):
        pt: Path = execution_path('testLogData')
        pm = PsudoMain({'rmslogdir': str(pt), 'moduleid': '1234a', 'age': 0, 'program': './tests/testecho.bat',
                        'relay': '01', 'powerofftime': 1, 'emsub': 'just a test...ignore',
                        "fromemail": "junk.r@gmail.com",
                        "toemail": [
                            "junk@gmail.com",
                            "junk@outlook.com",
                            "junk.r@gmail.com"
                        ],
                        'emailonly': True,
                        'testing': True,
                        'testingaccount': 'junk',
                        'password': 'password'
        })
        
        from myemail import MyEmail
        acnt:MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid='K7RVM.R',
            password='pEPbjVu4hkZctZJKVWlJ', 
            url='smtp.gmail.com:587')
        pm.prams['emacnt']=acnt 
        aa=None
        aa= pm._send_email(True)
        self.assertTrue(aa)
        aa=pm._send_email(False)
        self.assertEqual(1,len(aa))
        cc = aa.get('sentem')
        self.assertTrue('just a test...ignore' in cc)
        
        pass 


if __name__ == '__main__':
    unittest.main()
