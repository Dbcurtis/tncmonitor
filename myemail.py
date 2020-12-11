#!/usr/bin/env python3
""" email

    Module to send e-mail via a goggle account
"""
from typing import Any, Union, Tuple, Callable, TypeVar, Generic, Sequence, Mapping, List, Dict, Set, Deque
import smtplib  #* see: https://docs.python.org/3.8/library/smtplib.html
from smtplib import SMTP, SMTPAuthenticationError
#from email.message import EmailMessage
import logging
from time import asctime, localtime, time
#import pathlib
from collections import namedtuple

LOGGER = logging.getLogger(__name__)


class MyEmail:
    """MyEmail
    A class for sending email meesages via a google account

    """

    # named tuple arguments
    Email_Arg = namedtuple('Email_Arg', "subj fremail addto addcc")
    Accnt_Arg = namedtuple('Accnt_Arg', "accountid password")

    def __init__(self, acct: Accnt_Arg, emdata: Email_Arg):
        """MyEmail(tolist)

        the emdata contains the subject, the from-address, the to-addresses, and the cc-addresses
        the acct contains the accountid, and its password
        No checks made on correctness of the addresses

        The content of the email is inserted by the send method
        """

        self.emdata: MyEmail.Email_Arg = emdata
        self.accnt: MyEmail.Accnt_Arg = acct
        self.problems:Dict[str,str]={}
        
        def _make_header()->str:
            """
                Returns:
                    str: similar to:
                        From: emailadd \n
                        To: emailadd \n
                        CC: emailadd \n 
                        Subject: string \n\n 
            """
            header:str = f'From: {self.emdata.fremail}\n'  # from_addr
            aa:Any = self.emdata.addto
            if isinstance(aa,list):
                aa= ", ".join(self.emdata.addto)
                
            tostr:str = aa
            header += f'To: {tostr.strip()}\n'
            
            aa = self.emdata.addcc
            if aa:
                if isinstance(aa,list):
                    aa= ", ".join(self.emdata.addto)

                ccstr:str = aa.strip()
                
                if ccstr:
                        header += f'Cc: {ccstr}\n'
                    
            header += f'Subject: {self.emdata.subj.strip()}\n\n'
            return header 
        
        self.header:str = _make_header()
        self.lastemail:str = None  #! TODO perhaps have this be current email and add a fixed length dequeue for history
        

    def __str__(self) -> str:
        return f'Header: {self.header}'

    def __repr__(self) -> str:
        return self.__str__()

    def send(self, msg: str)->Dict[str,str]:
        """send(msg:str)

        Args:
            msg (str): text that is to be in the body of the email

        Returns:
            Dict[str, str]: with any problems... Generally empty
        """        

        #---------------------
        def _send_email(msg: str, mtpserver='smtp.gmail.com:587')->Dict[str,str]:
            """_send_email(mst,mtpserver=)

            Args:
                msg (str): is the text for the body of the email
                mtpserver (str, optional): is a SMTP serfer address, Defaults to 'smtp.gmail.com:587' for google smtp

            Returns:
                Dict[str,str]: [description]
            """

            #---------------------               
            def makemessage() -> str:
                """makemessage()
                
                combines the self.header with the msg
                
                """
                mess:str = f'{self.header}{msg}'
                return mess
            #---------------------

            logmsg:List[str] = ['Attempt to send e-mail at ',
                        asctime(localtime(time())), ' ']  # will join the list after it s built
            #problems:Dict[str,str] = {}

            #message:str = makemessage()    
            self.lastemail =  makemessage()       

            server:SMTP = SMTP(mtpserver)
            try:
                server.starttls()  # start tls protection
                server.login(self.accnt.accountid, self.accnt.password)
                self.problems = server.sendmail(
                    self.accnt.accountid, self.emdata.addto, self.lastemail)  # send the message
                
            except (KeyboardInterrupt, SystemExit):
                raise

            except SMTPAuthenticationError as _:
                st_=f'error: {str(_.smtp_code)}, err: {_.smtp_error.decode()}'
                    # LOGGER.critical(st_)
                self.problems['SMTPError'] = st_
                raise _
            
            finally:
                server.quit()
                if self.problems:
                    logmsg.append('failed')
                else:
                    logmsg.append('succeeded')

                lmsg:str = ''.join(logmsg)
                LOGGER.info(lmsg)
            return self.problems
        #---------------------
        
        self.problems={}
        return _send_email(msg)


if __name__ == '__main__':

    acntarg: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
        "your account login", "your account password", )
    emarg: MyEmail.Email_Arg = MyEmail.Email_Arg(
        "test email- ignore", "your from email address", ['receiver1@gmail.com', 'receiver2@gmail.com'], [],)
    acntarg: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg( # ! delete this line
        "K7RVM.R", "pEPbjVu4hkZctZJKVWlJ", )  # ! delete this line
    emarg: MyEmail.Email_Arg = MyEmail.Email_Arg( # ! delete this line
        "test email- ignore", "k7rvm.r@gmail.com", ["dbcurtis@gmail.com", "k7rvm.r@gmail.com"], ["rita.derbas@gmail.com"],)  # ! delete this line
    EM = MyEmail(acntarg, emarg)
    MY_PROBLEMS = EM.send('Email to test the myemail.py main call\n')
    if MY_PROBLEMS:
        for e, p in MY_PROBLEMS.items():
            print(f'{e} -> {p}')