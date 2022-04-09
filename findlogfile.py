#!/usr/bin/env python3.10
""" findlogfile

Module to find the RMS log file

"""

import logging
import os
import subprocess
# import sys
# import time
# from collections import deque, namedtuple
from pathlib import Path
from subprocess import CompletedProcess
from time import sleep
from typing import (Any,  Dict,  List,  NamedTuple, )
# from typing import (Any, Callable, Dict, Generic, List, Mapping, Sequence,
#                     Tuple, NamedTuple, TypeVar, Union,)

LOGGER = logging.getLogger(__name__)
VERSION_DATE = 'findlogfile.py v0.1 20201203'
LOG_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__))) / 'logs'
LOG_FILE: Path = LOG_DIR / 'findlogfile'

class DataFileData(NamedTuple):
    date:str
    fname:str

class FindLogFile:
    """FindLogFile

    Used to find the most recient 'TNC Events' log file in the logging directory,
    and to be able to index to earlier versions (for debugging purposes)
    """

    def __init__(self, prams: Dict[str, str], dirpath: Path):
        """__init__(self, prams, dirpath)

        prams is the paramiter dictionary, use dirpath instead of the prams value
        if it has been set by the caller.
        dirpath is a Path to the directory which contains the logging files

        The prarm dict is explained in the README.rst file
        """
        self.prams: Dict[str, str] = prams
        self.dirpath: Path = dirpath

    def __str__(self) -> str:
        return str(self.dirpath)

    def __repr__(self) -> str:
        return '%s(%r)' % (self.__class__, self.__dict__)

    def doit(self, age: int| str | None = None) -> Path | None:
        """doit

        finds the RMS Packet TNC Events files, orders by date and retuns the newest one if age = 0 or None,
        and as age increases, older and older files,

        return None if illegal age or if no RMS Packet TNC Events in the directory
        returns path to file if legal age
        """

        if not self.dirpath.is_dir():  # should have been tested at the main routine
            LOGGER.warning(
                'self.dirpath (%s) is not a directory', str(self.dirpath))
            return None

        # note if age is 0 it is false, and 0 is a valid value
        if age is None:  # really do not like None as an age, so make it 0
            age = self.prams.get('age')
            if age is None:
                age =0
        age=int(age)

        _files: List[str] = []
        # return from walk is s 3-tuple (dirpath,dirnames, filenames) we only need the filenames.. its a list
        for (_, _, filenames) in os.walk(self.dirpath):  # gets the filenames from the first directory
            _files.extend(filenames)
            break

        _tnceventfiles: List[str] = [_ for _ in _files if 'TNC Events' in _]
        if not _tnceventfiles:
            return None

        #data_file_data:DateFileData = NamedTuple('DateFileData', 'date fname')

        # the file names are of the form "RMS Packet Autoupdate YYYYMMDD.log"
        def _gendfd(arg:str) -> DataFileData:  # generate dated file data
            _date:str = arg.split("RMS Packet TNC Events ")[1][0:8]  # this selects the 8 char date
            dfd:DataFileData  = DataFileData(_date, arg)
            return dfd

        _datafile_ts: List[DataFileData] = [_gendfd(_) for _ in _tnceventfiles]

        _ll:List[DataFileData] = sorted(_datafile_ts, key=lambda dfd: dfd.date)
        _ll.reverse()
        result:Path = self.dirpath
        if isinstance(age,int): 
            iage:int = int(age)
            if iage < 0 or iage >= len(_ll):
                return None
            
            result = result / Path(_ll[iage].fname)
        return result


def _main():
    """_main()

    [summary]
    """
    _cwd: Path = Path.cwd()
    _dip: Path = _cwd / 'tests' / 'testLogData'
    # flf:FindLogFile = FindLogFile({},_dip)
    # tktfile:Path = flf.doit(0)
    tktfile: Path | None = FindLogFile({}, _dip).doit('0')
    expected: str = 'M:\\Python\\Python3_packages\\tncmonitor\\tests\\testLogData\\RMS Packet TNC Events 20180615.log'
    if expected == str(tktfile):
        print('found expected file')
    else:
        print(f'found wrong file {str(tktfile)}')


if __name__ == '__main__':
    THE_LOGGER = logging.getLogger()

    try:
        print(f'Starting {VERSION_DATE}')
        _main()

    except IOError as ioe:
        THE_LOGGER.exception(ioe)
        print('findlogfile.py I/O error')

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
