#!/usr/bin/env python3
""" makehtml.py

Module to convert generate a README.html from the README.rst file.
"""

import docutils.core


def main():
    docutils.core.publish_file(
        source_path="README.rst",
        destination_path="README.html",
        writer_name="html")


if __name__ == '__main__':
    main()
