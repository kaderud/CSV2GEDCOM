#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CSV to GEDCOM converter
   This program converts a preformatted CSV file to a compatible GEDCOM v5.5.1 file
"""

__author__ = "Ferenc Bodon and Christian Kaderud"
__credits__ = ["Ferenc Bodon", "Christian Kaderud"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Christian Kaderud"
__email__ = "christian@cklabs.org"
__status__ = "Production"

import sys
import pyexcel as pe
from CsvParser2Gedcom import FamilyTreeMapping

def main(argv):
    if len(argv) < 1:
        print("Missing CSV file!", file=sys.stderr)
        return
    t = pe.get_records(file_name=argv[0])
    ft = FamilyTreeMapping(t)
    ft.printGedcom()

if __name__ == "__main__":
   main(sys.argv[1:])
