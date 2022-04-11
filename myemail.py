#!/usr/bin/env python3.10
""" email

    Module to send e-mail via a goggle account
"""
from typing import (Any, List, Dict, NamedTuple, Deque, Generator,)
#from typing import (Any, Union, Tuple, Callable, TypeVar, Generic, Sequence, Mapping, List, Dict, Set, Deque,)
import smtplib  # * see: https://docs.python.org/3.8/library/smtplib.html
from smtplib import (SMTP, SMTPAuthenticationError, SMTPServerDisconnected,)
from collections import deque
import logging
from time import (asctime, localtime, time,)
import textwrap

LOGGER = logging.getLogger(__name__)


class MyEmail:
    """MyEmail
    A class for sending email meesages via a google account

    """

    @staticmethod
    def _limit_line_length(instr:str)->str:
        return  textwrap.fill(instr)

    # named tuple that contains the from, to and cc addresses for the email
    class Emailarg(NamedTuple):
        subj: str = ''
        fremail: str = ''  # from email
        addto: List[str] | str = ''
        addcc: List[str] | str = ''

    # named tuple that contains the login information for the SMTP server
    class Accntarg(NamedTuple):
        accountid: str = ''
        password: str = ''
        url: str = ''

    def __init__(self, acct: Accntarg, emdata: Emailarg):
        """MyEmail(tolist)

        the emdata contains the subject, the from-address, the to-addresses, and the cc-addresses
        the acct contains the accountid, and its password
        No checks made on correctness of the addresses

        The content of the email is inserted by the send method
        """

        self.emdata: MyEmail.Emailarg = emdata
        self.accnt: MyEmail.Accntarg = acct
        self.problems: Dict[Any, Any] = {}
        self.currentemail: str | None = None
        self.hist: Deque[Any] = deque([Any], maxlen=20)
        self.lastemail: str | None = None

        def _make_header() -> str:
            """
                Returns:
                    str: similar to:
                        From: emailadd \n
                        To: emailadd \n
                        CC: emailadd \n 
                        Subject: string \n\n 
            """
            header: str = f'From: {self.emdata.fremail}\n'  # from_addr
            _aa: Any = self.emdata.addto
            if isinstance(_aa, list):
                _aa = ", ".join(self.emdata.addto)

            tostr: str = _aa
            header += f'To: {tostr.strip()}\n'

            _aa = self.emdata.addcc
            if _aa:
                if isinstance(_aa, list):
                    _aa = ", ".join(self.emdata.addcc)

                ccstr: str = _aa.strip()

                if ccstr:
                    header += f'Cc: {ccstr}\n'

            header += f'Subject: {self.emdata.subj.strip()}\n\n'
            return header

        self.header: str = _make_header()
        # ! TODO perhaps have this be current email and add a fixed length dequeue for history

    def __str__(self) -> str:
        return f'Header: {self.header}'

    def __repr__(self) -> str:
        return self.__str__()

    def send(self, msg: str) -> Dict[str, str]:
        """send(msg:str)

        Args:
            msg (str): text that is to be in the body of the email

        Returns:
            Dict[str, str]: with any problems... Generally empty
        """

        # ---------------------
        def _send_email(msg: str) -> Dict[str, str]:
            """_send_email(mst,mtpserver=)

            Args:
                msg (str): is the text for the body of the email
                mtpserver (str, optional): is a SMTP serfer address, Defaults to 'smtp.gmail.com:587' for google smtp


            Returns:
                Dict[str,str]: [description]
            """

            # ---------------------
            def makemessage() -> str:
                """makemessage()

                combines the self.header with the msg

                """
                # RFC 5322 2.1.1 suggests 78 characters per line
                #amsg:str = self._limit_line_length(msg)
                amsg: str = textwrap.fill(msg)

                mess: str = f'{self.header}{amsg}'
                return mess
            # ---------------------

            logmsg: List[str] = [
                'Attempt to send e-mail at ',
                asctime(localtime(time())), ' '
            ]  # will join the list after it is built

            self.currentemail = makemessage()
            try:
                with SMTP(self.accnt.url) as server:
                    server.starttls()  # start tls protection
                    server.login(self.accnt.accountid, self.accnt.password)
                    self.problems= server.sendmail(
                        self.accnt.accountid, self.emdata.addto, self.currentemail)  # send the message
                    self.lastemail=self.currentemail

            except (KeyboardInterrupt, SystemExit):
                raise

            except SMTPServerDisconnected as _:
                st_ = str(_)
                # LOGGER.critical(st_)
                self.problems['SMTPError0'] = st_
                raise _

            except SMTPAuthenticationError as _:
                st_ = f'error: {str(_.smtp_code)}, err: {_.smtp_error}'  #do I need a decode here?
                # LOGGER.critical(st_)
                self.problems['SMTPError1'] = st_
                raise _

            except BaseException as _:
                a = 0

            finally:
                #server.quit()
                if self.problems:
                    logmsg.append('failed')
                else:
                    logmsg.append('succeeded')

                lmsg: str = ''.join(logmsg)
                LOGGER.info(lmsg)
            return self.problems
        # ---------------------

        self.problems = {}
        return _send_email(msg)


if __name__ == '__main__':
    #from loadprams import get_prams

    acntarg: MyEmail.Accntarg = MyEmail.Accntarg(
        "your account login", "your account password", "your SMTP Server url")
    emarg: MyEmail.Emailarg = MyEmail.Emailarg(
        "test email- ignore", "your from email address", ['receiver1@gmail.com', 'receiver2@gmail.com'], [],)
    acntarg: MyEmail.Accntarg = MyEmail.Accntarg(  # ! delete this line
        'K7RVM.R', 'pEPbjVu4hkZctZJKVWlJ', 'smtp.gmail.com:587')  # ! delete this line
    emarg: MyEmail.Emailarg = MyEmail.Emailarg(  # ! delete this line
        "test email- ignore", "k7rvm.r@gmail.com", ["dbcurtis@gmail.com", "k7rvm.r@gmail.com"], ["rita.derbas@gmail.com"],)  # ! delete this line
    EM = MyEmail(acntarg, emarg)
    MY_PROBLEMS = EM.send('Email to test the myemail.py main call\n')
    if MY_PROBLEMS:
        for e, p in MY_PROBLEMS.items():
            print(f'{e} -> {p}')
