#!/usr/bin/env python3
"""
Test file for myemail
"""
import os
import sys
from typing import List, Any, Dict, Tuple
import platform
from time import sleep
from smtplib import SMTP, SMTPAuthenticationError
#import subprocess
#from subprocess import CompletedProcess
#import inspect
import unittest
from pathlib import Path

ppath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ppath)

import myemail
from myemail import MyEmail


class TestMyEmail(unittest.TestCase):
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

    def test_01instant(self):
        """test_01instant

        """
        acct1: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid="jjj", password="kkk")
        emdata1: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj="mysubject1",
            fremail="somebody@junk.jnk",
            addto="to@junk.jnk",
            addcc="cc@junk.jnk",
        )

        bbb = "Accnt_Arg(accountid='jjj', password='kkk')"
        aaa = "Email_Arg(subj='mysubject1', fremail='somebody@junk.jnk', addto='to@junk.jnk', addcc='cc@junk.jnk')"

        self.assertEqual(bbb, str(acct1))
        self.assertEqual(aaa, str(emdata1))
        self.assertEqual("mysubject1", emdata1.subj)
        self.assertEqual("somebody@junk.jnk", emdata1.fremail)
        self.assertEqual("to@junk.jnk", emdata1.addto)
        self.assertEqual("cc@junk.jnk", emdata1.addcc)
        self.assertEqual("jjj", acct1.accountid)
        self.assertEqual("kkk", acct1.password)

        acct2: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid="jjjj", password="kkkk")
        emdata2: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj="mysubject2",
            fremail="somebody@junk.jnk",
            addto=["to1@junk.jnk", "to2@junk.jnk"],
            addcc=["cc1@junk.jnk", "cc2@junk.jnk"],
        )

        self.assertEqual("jjjj", acct2.accountid)
        self.assertEqual("kkkk", acct2.password)
        self.assertEqual(["to1@junk.jnk", "to2@junk.jnk"], emdata2.addto)
        self.assertEqual(["cc1@junk.jnk", "cc2@junk.jnk"], emdata2.addcc)

        mem:MyEmail = MyEmail(acct1, emdata1)
        stra:str = 'Header: From: somebody@junk.jnk\nTo: to@junk.jnk\nCc: cc@junk.jnk\nSubject: mysubject1\n\n' #str(mem)
        repra:str = 'Header: From: somebody@junk.jnk\nTo: to@junk.jnk\nCc: cc@junk.jnk\nSubject: mysubject1\n\n' # repr(mem)
        self.assertEqual(stra, str(mem))
        self.assertEqual(repra, repr(mem))
        
    def test_02send_badAccount(self):
        from myemail import MyEmail
        acct1: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid="jjj", password="kkk")
        emdata1: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj="mysubject1",
            fremail="somebody@junk.jnk",
            addto="to@junk.jnk",
            addcc="cc@junk.jnk",
        )
        mem = MyEmail(acct1, emdata1)
        problems:Dict[str,str]={}
        try:
            problems=mem.send("this is my body text")
            self.fail('did not detect wrong account at server login')
        
        except SMTPAuthenticationError as _:
            self.assertTrue('error: 535' in mem.problems.get('SMTPError'))
            
        except Exception as ex:
            self.fail(str(ex))
            
        finally:
            self.assertEqual(1,len(mem.problems))
            self.assertFalse(problems)     
    
    def test_03send_goodAccount(self):
        print('remove private data from this test')
        from myemail import MyEmail
        accnt:str = "K7RVM.R"
        psswd:str = "pEPbjVu4hkZctZJKVWlJ"
        fmem:str = "k7rvm.r@gmail.com"
        to:str = "dbcurtis@gmail.com"
        cc:str = "rita.derbas@gmail.com"
        sub:str = "test of a good send -- ignore"
        
        
        acct1: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid=accnt, password=psswd)
        emdata1: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj=sub,
            fremail=fmem,
            addto=to,
            addcc=cc,
        )
        mem:MyEmail = MyEmail(acct1,emdata1)
        problems:Dict[str,str]={}
        try:
            problems = mem.send("body, just ignore this message")
            self.assertFalse(problems)
            aa:str ='From: k7rvm.r@gmail.com\nTo: dbcurtis@gmail.com\nCc: rita.derbas@gmail.com\nSubject: test of a good send -- ignore\n\nbody, just ignore this message' #mem.lastemail
            self.assertEqual(aa,mem.lastemail)
        
        except SMTPAuthenticationError as _:
            self.fail(f'authn: {str(_)}')
            
        except Exception as ex:
            self.fail(str(ex))
            
        finally:
            self.assertFalse(mem.problems)
            self.assertFalse(problems)  
            
    def test_04send_goodAccountmulti(self):
        print('remove private data from this test')
        from myemail import MyEmail
        accnt:str = "K7RVM.R"
        psswd:str = "pEPbjVu4hkZctZJKVWlJ"
        fmem:str = "k7rvm.r@gmail.com"
        to:str = ["dbcurtis@gmail.com","wesf@outlook.com"]
        cc:str = ["rita.derbas@gmail.com","dbcurtis@gmail.com"]
        sub:str = "test of a good send multiple to and cc"
        
        acct1: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            accountid=accnt, password=psswd)
        emdata1: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj=sub,
            fremail=fmem,
            addto=to,
            addcc=cc,
        )
        
        problems={}
        mem:MyEmail = MyEmail(acct1,emdata1)
        try:
            problems = mem.send("body, test multiple cc and to just ignore this message")
            self.assertFalse(problems)

        
        except SMTPAuthenticationError as _:
            self.fail(f'authn: {str(_)}')
            
        except Exception as ex:
            self.fail(str(ex))
            
        finally:
            self.assertFalse(mem.problems)
            self.assertFalse(problems)  
            

if __name__ == '__main__':
    unittest.main()
