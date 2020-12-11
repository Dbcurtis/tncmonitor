#!/usr/bin/env python3
""" rst2html

    generate a README.html file from the README.rst file 
"""
from typing import Any, Union, Tuple, Callable, TypeVar, Generic, Sequence, Mapping, List, Dict, Set, Deque
import docutils.core
import logging
import logging.handlers


LOGGER = logging.getLogger(__name__)
THE_LOGGER = logging.getLogger()

def _main():
    docutils.core.publish_file(
        source_path="README.rst",
        destination_path="README.html",
        writer_name="html"
    )
    print('generated README.html from README.rst')


if __name__ == '__main__':
    try:

        _main()

    except IOError as ioe:
        print('rst2html.py I/O error')

    except ValueError as _:
        THE_LOGGER.exception(_)
        print(_)

    except (KeyboardInterrupt, SystemExit) as _:
        pass
