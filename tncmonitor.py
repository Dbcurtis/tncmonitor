#!/usr/bin/env python3
""" tncmonitor

    See the README.rst file
"""
from typing import Any, Union, Tuple, Callable, TypeVar, Generic, Sequence, Mapping, List, Dict, Set, Deque
import os
import sys
from collections import namedtuple
import platform
import argparse
import json
import logging
import logging.handlers
import copy
from time import asctime, localtime, time, sleep
from pathlib import Path
from resettnc import ResetTNC
import myemail
from myemail import MyEmail
from findlogfile import FindLogFile
from check4noInit import Check4noInit
from loadprams import  get_prams, setup_parser

INResponse = namedtuple('INResponse', 'ok rescode')

LOGGER = logging.getLogger(__name__)
VERSION_DATE: str = 'tncmonitor v0.2 20201126'

LOG_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__))) / 'logs'
_dirok: bool = False

try:
    LOG_DIR.mkdir(exist_ok=True)
    _dirok = True
    
except FileNotFoundError as fnfe:
    print(f'Parent file not found in {LOG_DIR}: {fnfe}')
    raise fnfe

if not _dirok and LOG_DIR.is_file():
    print(f'Specified path is not to a directory: {LOG_DIR}')
    raise FileExistsError(f'{LOG_DIR} exists and is not a directory')

LF_HANDLER = logging.handlers.RotatingFileHandler(
    LOG_DIR / 'tncmonitor',
    maxBytes=100000,
    backupCount=5,
)

LC_HANDLER = logging.StreamHandler()
LF_FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
LC_FORMATTER = logging.Formatter('%(name)s: %(levelname)s - %(message)s')
THE_LOGGER = logging.getLogger()

_FOR_10_MIN: int = 60 * 10
_FOR_1_MIN: int = 60

def _send_end_email(prams:Dict[str, Any]):
    """_send_end_email()
    """
    if prams:
        emheader: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj=f"@{asctime(localtime(time()))}: { prams.get('program')} ending ",
            fremail=prams.get('fromemail'),
            addto=prams.get('toemail'),
            addcc=None,
        )
        _em = myemail.MyEmail(prams.get('emacnt'),emheader)
        _em.send(
            f'The {VERSION_DATE} is Ending at {asctime(localtime(time()))}')

def _send_start_email(prams:Dict[str, Any]):
    """[summary]
    """
    if prams:
        emheader: MyEmail.Email_Arg = MyEmail.Email_Arg(
            subj=f"@{asctime(localtime(time()))}: {prams.get('program')} starting ",
            fremail=prams.get('fromemail'),
            addto=prams.get('toemail'),
            addcc=None,
        )
        _em = myemail.MyEmail(prams.get('emacnt'),emheader)
        _em.send(
            f'The {VERSION_DATE} is Starting at {asctime(localtime(time()))}')

class PsudoMain:
    """PsudoMain(prams:Dict)

    """

    def __init__(self, prams):
        """__init__(self, prams)
        prams is a dict with all the parameters
        """

        self.c4ni = None
        self.prams = copy.copy(prams)
        self.timeinc:List[float] = [0.0, 2 * 60.0, 10 * 60.0,
                        30 * 60.0, 60 * 60.0, 120 * 60.0]  # seconds between each email
        self.timeidx:int = 0
        self.time_of_last_email:float = None

    def __repr__(self)->str:
        return '%s(%r)' % (self.__class__, self.__dict__)

    def gettimeidx(self)->int:
        """gettimeids()

        """
        self.timeidx += 1
        if self.timeidx >= len(self.timeinc):
            self.timeidx = 0
        return self.timeidx

    def _send_email(self,donotsend:bool)->Dict[str, str]:
        """_send_email  

        routine to send the e-mail
        """
        timenow:float = time()
        self.time_of_last_email = timenow
        self.gettimeidx()
        problems: Dict[str, str]={}
        if not donotsend:
            emheader: MyEmail.Email_Arg = MyEmail.Email_Arg(
                subj=f"{self.prams.get('emsub')}",
                fremail=self.prams.get('fromemail'),
                addto=self.prams.get('toemail'),
                addcc=None,
            )
            
            if (self.prams.get('emacnt')):
                _em = myemail.MyEmail(self.prams.get('emacnt'), emheader)
                problems = _em.send(
                    f"@{asctime(localtime(timenow))}, {self.prams.get('emsub')}"
                )
                        
                if problems:
                    _l = ['']
                    _l.extend([k + ' -> ' + ss for k, ss
                                in problems.items()])
                    _msg:str = '\nError:**'.join(_l)
                    LOGGER.warning(_msg)
                else:
                    problems={'sentem':_em.lastemail}
            elif self.prams.get('testing'):
                problems['testing']='testing mode no email account info'
                
        else:
            problems['donotsend']=f'mailtime {asctime(localtime(timenow))}'
        return problems

    def doit(self, timers=None, count=None, age1:int=None, donotsend:bool=False):
        """doit

        timers is a tuple for setting the delay between reset attempts and check attempts
        default is 1 min (if an init problem detected) and 10 min if no problem

        count is used for testing
        age1 is used for testing
        """

        if timers is None or len(timers) < 2:
            timers = tuple(self.prams.get('timers'))
        if count is None:
            count = self.prams.get('count')
        if age1 is None:
            age1 = self.prams.get('age')

        #--------------------------
        def send_reset_email():
            """set_reset_email()

            """
            if self.time_of_last_email is None:
                self.timeidx = 0
                self._send_email(donotsend)
            else:
                nowis:float = time()
                nextsched:float = self.time_of_last_email + \
                    self.timeinc[self.timeidx]
                if nowis >= nextsched:
                    self._send_email(donotsend)
        #--------------------------
        def work():
            """work()

            does the work
            """
            emailonly: bool = self.prams.get('emailonly')

            self.c4ni: Check4noInit = Check4noInit(self.prams)
            tups: Check4noInit.Result = self.c4ni.doit(age=age1)
            if tups.status and tups.result:
                if emailonly:
                    send_reset_email()
                    sleep(timers[1])
                else:
                    ResetTNC(self.prams).doit()
                    send_reset_email()
                    sleep(timers[0])

            else:
                self.time_of_last_email = None
                sleep(timers[1])
        #--------------------------

        try:
            if count > 0:
                while count > 0:
                    work()
                    count -= 1
            else:
                while True:
                    work()
        except FileNotFoundError as fnf:
            LOGGER.fatal('cannot find the program file specified... Aborting ')
            raise fnf


def _logsetup():
    """_logsetup()

    Just reduces statment count in _main
    """
    LF_HANDLER.setLevel(logging.INFO)
    LC_HANDLER.setLevel(logging.ERROR)
    LC_HANDLER.setFormatter(LC_FORMATTER)
    LF_HANDLER.setFormatter(LF_FORMATTER)
    THE_LOGGER.setLevel(logging.DEBUG)
    THE_LOGGER.addHandler(LF_HANDLER)
    THE_LOGGER.addHandler(LC_HANDLER)

def internet_on() -> INResponse:
    import requests
    result: INResponse = INResponse(ok=False, rescode=None)

    for timeouta in [1.0, 5.0, 10.0, 15.0]:
        try:
            response = requests.get('http://www.google.com', timeout=timeouta)
            result = INResponse(ok=True, rescode=response)

        except requests.exceptions.RequestException as err:
            result = INResponse(ok=False, rescode=err)
    return result

def _main(startup_delay: float = None)->Dict[str,Any]:
    """_main(Startup_delay=None)

    Startup_delay is a float of the number of seconds to wait for the program to actually start
    sets up the logger, handles arguments and performs some checks
    also conditinoally sends the startup e-mail
    """

    _logsetup()

    loglevel = logging.CRITICAL
    loglevel = logging.ERROR
    loglevel = logging.WARNING
    #loglevel = logging.INFO
    #loglevel = logging.DEBUG
    #loglevel = logging.NOTSET
    
    LOGGER.setLevel(logging.INFO) 

    THE_LOGGER.info("""
****************************************************
tncmonitor executed as main
****************************************************""")


    THE_LOGGER.info('Current Path is: %s', str(os.path.abspath('.')))

    args: argparse.Namespace = setup_parser()
    _ = [THE_LOGGER.info('args:%s, %s', i[0], i[1])
            for i in vars(args).items()]
    
    loglevel = logging.WARNING
    LC_HANDLER.setLevel(loglevel)

    if args.logdebug:
        loglevel = logging.DEBUG
        LC_HANDLER.setLevel(loglevel)

    elif args.loginfo:
        loglevel = logging.INFO
        LC_HANDLER.setLevel(loglevel)

    if startup_delay:
        sleep(startup_delay)

    THE_LOGGER.info("""
    *****************************
    Starting %s
    *****************************
        """, VERSION_DATE)
    prams: Dict[str, Any] = get_prams(args)
    
    try:
        rms_log_path:Path = Path(prams.get('rmslogdir'))
        internetok: INResponse = internet_on()
        if not internetok.ok:
            THE_LOGGER.warning('Network error: ' + internetok.rescode)

        if prams['start_end_email']:
            failemail = True
            while failemail:
                try:
                    _send_start_email(prams)
                    failemail = False
                except:
                    THE_LOGGER.warning('startup email failed')
                    sleep(60)

        if rms_log_path.exists() and rms_log_path.is_dir():
            try:
                _f = []
                for (_, _, filenames) in os.walk(rms_log_path):
                    _f.extend(filenames)
                    break

                if _f is None or not _f:
                    THE_LOGGER.warning("RMS directory is empty")

            except (KeyboardInterrupt, SystemExit):
                raise
            
            except IOError as _e:
                print(_e.args)
                print('Input directory {} is not readable'.format(rms_log_path))
                THE_LOGGER.error(
                    'Input directory %s is not readable', rms_log_path)
                raise _e

            if ResetTNC(prams).cpi.returncode:
                msg = 'The Relay is not connected or misconfigured'
                LOGGER.critical(msg)
                print(msg)

            else:
                _pm = PsudoMain(prams)
                _pm.doit()

        else:
            msg = 'path {} either does not exist or is not a directory'.format(
                rms_log_path)
            print(msg)
            LOGGER.critical(msg)
    finally:
        return prams


if __name__ == '__main__':
    prams:Dict[str,Any] = {}
    try:
        print(f'Starting {VERSION_DATE}')
        prams=_main(startup_delay=12)  # =120)
        

    except IOError as ioe:
        THE_LOGGER.exception(ioe)
        print('tncmonitor.py I/O error')

    except ValueError as _:
        THE_LOGGER.exception(_)
        print(_)

    except (KeyboardInterrupt, SystemExit) as _:
        pass

    if prams.get('start_end_email'):
        _send_end_email(prams)

    print("Exiting")
    THE_LOGGER.info("""
    *****************************
    EXITING %s
    *****************************
        """, VERSION_DATE)
