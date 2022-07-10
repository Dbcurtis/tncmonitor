#!/usr/bin/env python3.10
""" json2yaml

module to open a .json file and convert to .yml

"""

import sys
from typing import (Any, Dict,)
# from typing import (Any, Union, Tuple, Callable, TypeVar, Generic,
#                     Sequence, Mapping, List, Dict, Set, Deque,)

from pathlib import Path
import argparse
import json
import yaml
import logging

LOGGER = logging.getLogger(__name__)


def setup_parser() -> argparse.Namespace:
    """_setup_parser()

    defines the parser and generates the parsed args
    """
    _parser = argparse.ArgumentParser(
        description='JSON to YAML Convertor')

    _parser.add_argument(
        '-li', '--loginfo',
        help='enable INFO logging',
        action="store_true",)

    _parser.add_argument(
        '-ld', '--logdebug',
        help='enable DEBUG logging',
        action="store_true",)

    _parser.add_argument(
        'jinfile', default='sys.stdin', action='store',
        help='input parameter file JSON path',)

    _parser.add_argument(
        'youtfile', default='sys.stdin', action='store',
        help='output parameter file YAML path',)

    result: argparse.Namespace
    try:
        result: argparse.Namespace = _parser.parse_args(args)
    except:
        jj = sys.exc_info()
        a = 0

    return result


def json2yaml():
    json_path: Path = Path('tncprams.json')
    if not (json_path.exists() and json_path.is_file()):
        raise ValueError(f'{json_path} does not exist or is not a file')

        # ? need to do the loads here as windows path did not work
    result: Dict[str, Any] = json.loads(json_path.read_text())

    yaml_path: Path = Path('tncprams.yaml')
    with open(yaml_path, 'w') as fl:
        docs = yaml.dump(result, fl, sort_keys=True)
        a = 0
    a = 0


def ymal2read():
    yaml_path: Path = Path('prototypetncprams.yaml')
    data: Dict[str, Any]
    with open(yaml_path, 'r') as fl:
        data = yaml.full_load(fl)

    a = 10
    pass


def _main():
    # #ns: argparse.Namespace = setup_parser()
    # # verify the path is to an existing file
    # json_path: Path = Path('tncprams.json')
    # if not (json_path.exists() and json_path.is_file()):
    #     raise ValueError(f'{json_path} does not exist or is not a file')

    #     # ? need to do the loads here as windows path did not work
    # result: Dict[str, Any] = json.loads(json_path.read_text())

    # yaml_path: Path = Path('tncprams.yaml')
    # with open(yaml_path, 'w') as fl:
    #     docs = yaml.dump(result, fl, sort_keys=True)
    #     a = 0
    # a = 0

    # json2yaml()
    ymal2read()
    a = 0

    pass


if __name__ == '__main__':
    THE_LOGGER = logging.getLogger()

    try:
        _main()  # does nothing

    except IOError as ioe:
        THE_LOGGER.exception(ioe)
        print('json2yaml I/O error')

    except ValueError as _:
        THE_LOGGER.exception(_)
        print(_)

    except (KeyboardInterrupt, SystemExit):
        pass

    print("Exiting")
