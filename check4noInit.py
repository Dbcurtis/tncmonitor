#!/usr/bin/env python3.10
""" check4noInit

Module to read the RMS log file and find error meessages

"""
import logging
import os
import subprocess
#from dataclasses import dataclass
# import sys
# import time
from typing import (NamedTuple, Dict, List, Any,)
#from collections import deque, namedtuple
from pathlib import Path
# from subprocess import CompletedProcess
#from time import sleep
import copy

# from typing import (Any, Callable, Dict, Generic, List, Mapping, Sequence,
#                     Tuple, TypeVar, Union)
#     Sequence, Mapping, List, Dict, Set, Deque
from findlogfile import FindLogFile

LOGGER = logging.getLogger(__name__)
VERSION_DATE = 'check4noInit.py v0.2 20220403'
LOG_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__))) / 'logs'
LOG_FILE: Path = LOG_DIR / 'check4noInit'

class Result(NamedTuple):
    result:bool
    status:bool
    dl:str|None
    
 
    
    

class Check4noInit:
    """Check4noInit

    Class to check for no initialization errors from the RMS logfile
    Once doit is called, filepath and detectedline are filled and can be accessed
    """
    

    def __init__(self, prams: Dict[str, str], dirpath: Path|None =None):
        """__init__(self, dirpath)

        dirpath is a Path to the directory with the logging files used for debugging.
        The Path usually used, is obtained from the rmslogdir key of the prams dict.
        dirpath is usually used for debugging.

        The prarm dict is explained in the README.rst file

        """
        self.prams: Dict[str, str] = copy.copy(prams)
        if dirpath is None:
            self.dirpath = Path(self.prams.get('rmslogdir', os.getcwd()))
        else:
            self.dirpath = dirpath

        self.filepath: Path|None = None
        self.detectedline = None

    def __repr__(self) -> str:
        return '%s(%r)' % (self.__class__, self.__dict__)

    def __str__(self) -> str:
        return f'path: {self.filepath}, dline: {self.detectedline}'

    def doit(self, age:Any=None) -> Result:
        """doit

        age is used for debugging to select files other than the current one
        reads the selected RMS Packet TNC Events file backwards and
        returns (result,status,detected line) Namedtuple (.result, .status, .dl)
        result is (false,true, dl) if *** Ready, *** Closing, *** CONNECTED,
            *** DISCONNNECTED, or *** KPC3+ initialization successful
        result is (true,true,dl) if initialization failed
        result is (true,false,None) if initialization file is indeterminate

        """
        self.filepath = FindLogFile(self.prams, self.dirpath).doit(age)
        self.detectedline = None
        result: Result = Result(True, False, None)

        if self.filepath is not None:
            linesraw: List[str] = []
            lines: List[str] = []
            with self.filepath.open() as log:
                linesraw = log.readlines()

            lines = [line.strip() for line in linesraw]
            lines.reverse()
            # ?
            # ? The returns in the ifs within the for are used to simplify the
            # ? code because of the No detection logger message should only happen after
            # ? all the lines are read, but once the first trigger line is found, no need to complete reading
            # ? the entire file
            # ?
            for _ in lines:
                if '*** Closing - Please standby...' in _ \
                    or '*** CONNECTED ' in _ \
                    or '*** DISCONNECTED' in _ \
                        or '*** KPC3+ initialization successful' in _ \
                        or '*** Ready' in _:
                    self.detectedline = _
                    LOGGER.debug('Detected %s', self.detectedline)
                    result = Result(False, True, self.detectedline)
                    # return (False, True, self.detectedline )
                    return result

                elif '*** KPC3+ initialization failed' in _:
                    self.detectedline = _
                    LOGGER.warning('%s', self.detectedline)
                    result = Result(True, True, self.detectedline)
                    # return (True, True, self.detectedline )
                    return result

        LOGGER.debug('No detection')
        return result


def _main():
    """_main()
        * prints out 'Starting' and the filename and version id

    """
    test_dir: Path = Path(os.getcwd())
    lastpart = Path.cwd().parts[-1]

    if lastpart != 'tests' or lastpart != 'tncmonitor':
        if lastpart == 'tncmonitor':
            test_dir = Path.cwd() / 'tests'
        else:
            test_dir = Path.cwd()
    else:
        print('Fail not on .../tncmonitor/tests/')
        raise ValueError

    test_dir = test_dir / 'testLogData'
    try:

        prams: Dict[str, str] = {}
        c4init: Check4noInit = Check4noInit(prams, dirpath=test_dir)
        result: Result = c4init.doit()
        print(
            'next line should be "2018/06/15 02:06:49 [10] *** DISCONNECTED"')
        print(result.dl)

    except subprocess.TimeoutExpired as toe:
        THE_LOGGER.exception(toe)
        raise toe

    finally:
        pass


if __name__ == '__main__':
    THE_LOGGER = logging.getLogger()

    try:
        print(f'Starting {VERSION_DATE}')
        _main()

    except IOError as ioe:
        THE_LOGGER.exception(ioe)
        print('resettnc.py I/O error')

    except ValueError as _:
        THE_LOGGER.exception(_)
        print(_)

    except subprocess.TimeoutExpired as _:
        THE_LOGGER.exception(_)
        print(_)

    except (KeyboardInterrupt, SystemExit):
        pass

    print("Exiting")
    THE_LOGGER.info("""
    *****************************
    EXITING %s
    *****************************
        """, VERSION_DATE)
