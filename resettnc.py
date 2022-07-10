#!/usr/bin/env python3.10
""" resettnc

Module to reset a device by removing power
from the device and then
restoring power after a short delay.
"""
import os
#import sys
# from typing import (Any, NamedTuple, Tuple,  TypeVar, Generic, Sequence,
#                     Mapping, List, Dict, Set, Deque,)
from typing import (Any,  Tuple,  List, Dict,  Deque,)
import subprocess
from subprocess import CompletedProcess
import time
from time import sleep
from collections import deque
from pathlib import Path
import logging

LOGGER = logging.getLogger(__name__)
VERSION_DATE = 'resettnc.py v0.2 20201126'


class ResetTNC:
    """ResetTNC

    Class used to turn off the power of the TNC and then turn it back on
    """

    def __init__(self, prams: Dict[str, str],
                 debug_program: Path = Path(os.getcwd()),
                 hist_size: int = 20,):
        """[summary]

        Args:
            prams ([Dict[str,str]]): {'moduleid': 'modid',
            'relay': 'relaynum like 01',
            "program": "CommandApp_USBRelay",
            "powerofftime": str seconds,}
            debug_program ([type], optional): [description]. Defaults to None.
            hist_size is the size of the history deque

        Raises:
            subprocess.TimeoutExpired
        """
        self.prams: Dict[str, str] = prams
        if debug_program is None or debug_program.is_dir():
            self.program: Any = prams.get('program')
        else:
            self.program: Any = debug_program
        self.cpi:Any= None
        self.state: str = 'Unknown'
        self.history: Deque[Tuple[str, ...]] = deque(maxlen=hist_size)
        self.powerup()

    def __repr__(self) -> str:
        return '%s(%r)' % (self.__class__, self.__dict__)

    def __str__(self) -> str:
        return f'TNC prams:{self.prams}, state: {self.state}'

    def powerdown(self):
        """powerdown()

        Opens the relay by invoking a system subprocess
        Raises: 
            subprocess.TimeoutExpired: 
        """
        cmd: List[Any] = [self.program, self.prams.get(
            'moduleid'), 'open', self.prams.get('relay')]
        self.cpi = subprocess.run(
            cmd,
            input=None,
            timeout=1,
            shell=False,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='ascii'
        )
        if self.cpi.returncode:
            LOGGER.warning(
                "Powerdown returned error code %d",
                self.cpi.returncode)
            self.state = 'Unknown -EPD'
        else:
            self.state = 'PD'
        self.history.append(
            (time.asctime(time.localtime(time.time())), self.state))

    def powerup(self):
        """powerup()

        closes the relay by invoking a system subprocess

        Raises: 
            subprocess.TimeoutExpired: 
        """
        cmd: List[Any] = [self.program, self.prams.get(
            'moduleid'), 'close', self.prams.get('relay')]
        self.cpi = subprocess.run(
            cmd,
            input=None,
            timeout=1,
            check=False,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='ascii'
        )
        if self.cpi.returncode:
            LOGGER.warning(
                "Powerup returned error code %d",
                self.cpi.returncode)
            self.state = 'Unknown -EPU'
        else:
            self.state = 'PU'
        self.history.append(
            (time.asctime(time.localtime(time.time())), self.state)
        )

    def doit(self, delay:None|str|float=None):
        """doit

        Opens the relay, waits for delay seconds then closes the relay.
        delay is the number of seconds to leave the power off
        """
        delaya:str|float|None = 0.0 #str|float|None=0.0
        if self.cpi.returncode == 0:
            if delay is None:
                xx:Any = self.prams.get('powerofftime')
                assert isinstance(xx,str)
                delaya = float(xx)
            LOGGER.info('TNC Reset initiated')
            self.powerdown()
            sleep(float(delaya))
            self.powerup()


def _main():
    """_main() 
        * prints out 'Starting' and the filename and version id
        * checks that the subprocess works
        * asks user for:

            - Module Id 
            - Relay number
            - and if the above values are correct

        * opens and closes the relay 10 times, tells you to expect to hear clicking
        * tells you what the display should look like

    Raises:
        ValueError: If Python 3 is not installed or if the stderr from the subprocess does not include "Python 3"
    """
    try:
        CPI_TEST: CompletedProcess = subprocess.run(['python', '-V'],  # tests ability to run a subprocess.
                                                    input=None,
                                                    timeout=1,
                                                    check=False,
                                                    shell=False,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    encoding='ascii',
                                                    )

        if 'Python 3.' not in CPI_TEST.stdout:
            print(CPI_TEST)
            raise ValueError('Incorrect subprocess return, is Python 3 installed?')
        finished: bool = False
        modid: str = ''
        relayid: str = ''

        while not finished:
            modid = input('\n\nenter the module id: something like 3D0V2 ->\n')
            relayid = input(
                'enter the relay number as 2 digits like "01"-> \n')
            contval = input('Are the values above correct? (Y,N)->\n')
            if contval.upper().strip().startswith('Y'):
                finished = True

        _prms: Dict[str, str] = {
            # 'moduleid': '3X9XI',
            # 'relay': '01',
            'moduleid': modid,
            'relay': relayid,
            "program": "CommandApp_USBRelay",
            "powerofftime": '0.75',

        }
        TNC: ResetTNC = ResetTNC(_prms, hist_size=10)  # powers up on creation

        if TNC.cpi.returncode != 0:
            print("relay not connected or incorrectly configured")
            print(TNC.cpi)
        else:
            flag: int = 1
            cnt = 10
            print('You should hear the relay clicking...')
            while cnt > 0:  # opens and closes the relay 10 times.
                cnt -= 1
                TNC.doit()
                print(flag, end='')
                flag += 1
                sleep(float(_prms.get('powerofftime', 2)))
            # for a,b in TNC.history:
            #     print(a,b)

    except subprocess.TimeoutExpired as toe:
        THE_LOGGER.exception(toe)
        raise toe

    finally:
        pass


if __name__ == '__main__':
    THE_LOGGER = logging.getLogger()

    try:
        print(f"Starting {VERSION_DATE}")
        _main()
        print('\nThe Line above should be "12345678910"')

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
        raise

    print("Exiting")
    THE_LOGGER.info("""
    *****************************
    EXITING %s
    *****************************
        """, VERSION_DATE)
