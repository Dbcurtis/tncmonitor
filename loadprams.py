#!/usr/bin/env python3
""" loadprams

module to parse the arguments and load the parameter file

"""
import sys
from typing import Any, Union, Tuple, Callable, TypeVar, Generic, \
    Sequence, Mapping, List, Dict, Set, Deque

import subprocess
from pathlib import Path
import argparse
import json
import logging
from myemail import MyEmail

LOGGER = logging.getLogger(__name__)
VERSION_DATE = 'loadprams.py v0.2 20201213'

# the set of required keys in the pram dict
_legalpramkeyset: Set[str] = frozenset([

    "SMTPServer",
    "account",
    "password",
    "fromemail",
    "toemail",
    "rmslogdir",
    "program",
    "powerofftime",
    "moduleid",
    "relay",
    "emsub",
    "age",
    "count",
    "timers",

])

def setup_parser(args:List[str]=sys.argv) -> argparse.Namespace:
    """_setup_parser()

    defines the parser and generates the parsed args
    """
    _parser = argparse.ArgumentParser(
        description='Monitor TNC Error Logs')

    _parser.add_argument('-li', '--loginfo',
                         help='enable INFO logging',
                         action="store_true")

    _parser.add_argument('-ld', '--logdebug',
                         help='enable DEBUG logging',
                         action="store_true")

    _parser.add_argument('-eo', '--emailonly', default=False,
                         help='do not attempt to reset the TNC',
                         action="store_true")

    _parser.add_argument('pramfile', default='sys.stdin', action='store',
                         help='input parameter file JSON path')

    _parser.add_argument('-ese', '--emstartend', default=False, action='store_true',
                         help='enable sending an email when the program starts or ends')

    _parser.add_argument('-t', '--testdata', default=False, action='store_true',
                         help='use testing data in ./tests/testLogData')

    # _parser.add_argument('rnum', nargs='?', default=1, action='store',
    # help='Relay number on card, defaults to 1')

    # _parser.add_argument('rsn', nargs='?', default='3X9XI', action='store',
    # help='Relay card serial number defaults to 3X9XI')

    #result: argparse.Namespace = _parser.parse_args()

    return _parser.parse_args(args)


def get_prams(args: argparse.Namespace) -> Dict[str, Any]:
    """[summary]

    Args:
        args (argparse.Namespace): [description]

    Returns:
        Dict[str,Any]: [description]
    """
    def _remove_comments(fromjson:Dict[str,Any]):
        """[summary]

        Args:
            fromjson (Dict[str,Any]): [description]
        """
        # remove comment-like keys
        keyS:Set[str] = set(fromjson.keys())
        #ukeyL:List[str] = [k.upper() for k in keyS]
        ukeyS:Set[str]= set([k.upper() for k in keyS])
        cmtkeyL:List[str] = [_ for _ in ukeyS if "COMMENT" in _]
        if cmtkeyL:
            kstartingwithc:List[str] = [_ for _ in keyS if _.startswith("C") or _.startswith("c")]
            keystodelete:List[str] = []
            for k in kstartingwithc:
                if "COMMENT" in k.upper():
                    keystodelete.append(k)
            
            for k in keystodelete:
                fromjson.pop(k)
        
        
        item:Tuple[str,Any] = ()
        keyl:List[str]=[
                item[0] for item in fromjson.items() if isinstance(item[1],str) 
                and '--COMMENT--' in item[1].upper()
            ]                    
        for _ in keyl:
            fromjson.pop(_)
    

    def _setup_basic_prams(pram_path: Path) -> Dict[str, Any]:
        """[summary]

        Args:
            pram_path (Path): [description]

        Raises:
            ValueError: [description]
            ValueError: [description]

        Returns:
            Dict[str, Any]: [description]
        """
        # verify the path is to an existing file
        if not (pram_path.exists() and pram_path.is_file()):
            raise ValueError(f'{pram_path} does not exist or is not a file')

        # ? need to do the loads here as windows path did not work
        result: Dict[str, Any] = json.loads(pram_path.read_text())
        if result.get('isprototype', None):
            raise ValueError(f'{pram_path} is a prototype pramfile')
        
        # remove comment fields and values containing comments
        _remove_comments(result)

        acnt: MyEmail.Accnt_Arg = MyEmail.Accnt_Arg(
            result.get("account"),
            result.get("password"),
            result.get('SMTPServer', None),
        )
        result['emacnt'] = acnt  # this is the SMTP info
        
        ehead: MyEmail.Email_Arg = MyEmail.Email_Arg( # subj fremail addto addcc
            result.get('emsub'),
            result.get('fromemail'),
            result.get('toemail'),
            result.get('ccemail',None), 
        )
        result['emhead']=ehead
        return result

    # get the json paramiters and email info
    prams = _setup_basic_prams(Path(args.pramfile))
    prams['emailonly'] = args.emailonly  # add flags from the command line
    prams['testing'] = args.testdata
    prams['start_end_email'] = args.emstartend
    _pramskey: List[str] = list(prams.keys())
    #!  debugging line
    # pramskey.append('program')
    # pramskey.append('age')

    _pramsset: Set[str] = set(_pramskey)
    if len(_pramskey) != len(_pramsset):  # check for duplicate keys
        _pramskey.sort()
        _pkS: Set[str] = set(
            [
                _pramskey[i] for i in range(len(_pramskey)-1)
                if _pramskey[i] == _pramskey[i+1]
            ]
        )
        LOGGER.warning(f'Duplicate key(s) in pram file: {str(list(_pkS))}')

    _: Set[str] = set(_legalpramkeyset) & _pramsset
    if len(_legalpramkeyset) != len(_):
        # missing a required key in pram file
        _missingkeys: List[str] = list(_legalpramkeyset - _pramsset)
        _missingkeys.sort()
        LOGGER.critical(f'Missing required key(s): {str(_missingkeys)}')
        raise KeyError('missing required key(s) in pram file')

    return prams


def _main():
    print('this does nothing')


if __name__ == '__main__':
    THE_LOGGER = logging.getLogger()

    try:
        print("Starting {}".format(VERSION_DATE))
        _main()  # does nothing

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
