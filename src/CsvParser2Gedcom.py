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

import datetime
import calendar
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple

IDCOLNAME = 'ID'
FATHERIDCOL = 'Father ID'
MOTHERIDCOL = 'Mother ID'

HEADER = '''0 HEAD
1 SOUR GOD
2 VERS 6.0
2 NAME Genealogy ON DISPLAY
1 DATE {}
2 TIME {}
1 DEST MinSläkt
1 SUBM @SUBM1@
1 FILE MYFAMILY.GED
1 COPR Copyright (c) 2020 Christian K. Kaderud
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
1 LANG Swedish
1 NOTE This Gedcom file is not to be trusted and/or verified data.
2 CONC The data herein is converted from CSV (comma separated values)
2 CONC and some fields may contain invalid data or other mismatches.

0 @SUBM1@ SUBM
1 NAME Firstname Lastname
1 ADDR Street Address 1
2 CONT 90 210 BEVERLY HILLS
2 CONT USA
2 CONT Internet Email address:
2 CONT your@email.com
1 PHON +1-202-555-0170'''

TRAILER = '0 TRLR'


def convertDate(datum):
    return '{}'.format(str(datum).upper().replace('MAJ', 'MAY').replace('OKT', 'OCT'))


def printPlace(city,county,state):
    if ((city) or (county) or (state)):
        print(f"2 PLAC {city}{', ' if ((city) and (county)) else ''}{county}{', ' if state else ''}{state}")


@dataclass
class Family:
    id: int
    children: List[str]

    def addChildren(self, child):
        self.children.append(child)


@dataclass
class FamilyMapping:
    parentToFamily: Dict[Tuple[str, str], Family] # ID of Father, Mother Pair -> Family
    
    def __init__(self):
        self.parentToFamily = {}


    def addChildren(self, fatherID, motherID, childID):
        if (fatherID, motherID) in self.parentToFamily:
            self.parentToFamily[(fatherID, motherID)].addChildren(childID)
        else:
            self.parentToFamily[(fatherID, motherID)] = Family(len(self.parentToFamily) + 1, [childID])


    def getSpouseMap(self):
        res = {}
        for k, v in self.parentToFamily.items():
            if k[0]: # father might be missing
                res.setdefault(k[0], []).append(v.id)
            if k[1]: # mother might be missing
                res.setdefault(k[1], []).append(v.id)
        return res


    def printGedcom(self, ID2GedcomID):
        for k, v in self.parentToFamily.items():
            print('')
            print('0 @F{}@ FAM'.format(v.id))
            if k[0]: 
                if k[0] in ID2GedcomID: print('1 HUSB @I{}@'.format(ID2GedcomID[k[0]]))
                else: print("Missing individual {} registered as father.".format(k[0]), file=sys.stderr)
            if k[+1]: 
                if k[1] in ID2GedcomID: print('1 WIFE @I{}@'.format(ID2GedcomID[k[1]]))
                else: print("Missing individual {} registered as mother.".format(k[1]), file=sys.stderr)
            for child in v.children:
                print('1 CHIL @I{}@'.format(child))

hasKnownParent = lambda row: row[FATHERIDCOL] or row[MOTHERIDCOL]


class FamilyTreeMapping:
    __ID2GedcomID = {} # CSV ID -> Gedcom ID
    __famMap = FamilyMapping()
    __famSMap = {} # Gedcom ID -> list of family ID in which he/she is a spouse


    def __init__(self, t):
        """Create a FamilyTreeMapping object that supports printing a Gedcom file.

        arguments:
        t      -- the family tree data in a table-like format, i.e. each person is a map and people are contained in a list. This format is returned by function pyexcel.get_records.
        """
        self.t = t.copy()  
        self.__ID2GedcomID = {row[IDCOLNAME]: idx + 1 for idx, row in enumerate(t)}
        #self.trantab = str.maketrans("éáűúüőöóí", "eauuuoooi")

        for row in t:
            if not hasKnownParent(row): continue
            self.__famMap.addChildren(row[FATHERIDCOL], row[MOTHERIDCOL], self.__ID2GedcomID[row[IDCOLNAME]])

        self.__famSMap = self.__famMap.getSpouseMap()


    def __getFAMC(self, row):
        if hasKnownParent(row):
            return self.__famMap.parentToFamily[(row[FATHERIDCOL], row[MOTHERIDCOL])].id
        return None


    def printGedcom(self):
        print(HEADER.format(datetime.datetime.now().strftime('%d %b %Y').upper(), datetime.datetime.now().strftime('%H:%M:%S')))
        for row in self.t:
            print ('')
            print('0 @I{}@ INDI'.format(self.__ID2GedcomID[row[IDCOLNAME]]))
            print('1 NAME {} /{}/'.format(row['Given Names'], row['Surname']))
            print('1 SEX {}'.format('M' if row['Sex'] == 0 else 'F'))
            if row['Birth Date']:
                print('1 BIRT')
                print('2 DATE {}'.format(convertDate(row['Birth Date'])))
                printPlace(row['Birth City'],row['Birth County'],row['Birth State'])
            if row['Death Date']:
                print('1 DEAT')
                print('2 DATE {}'.format(convertDate(row['Death Date'])))
                printPlace(row['Death City'],row['Death County'],row['Death State'])
            if row['Burial Date']:
                print('1 BURI')
                print('2 DATE {}'.format(convertDate(row['Burial Date'])))
                printPlace(row['Burial City'],row['Burial County'],row['Burial State'])
            famc = self.__getFAMC(row)
            if not famc == None:
                print('1 FAMC @F{:,.0f}@'.format(famc))
            if row[IDCOLNAME] in self.__famSMap:
                for fmas in self.__famSMap[row[IDCOLNAME]]:
                    print('1 FAMS @F{}@'.format(fmas))
        self.__famMap.printGedcom(self.__ID2GedcomID)
        print('')
        print(TRAILER)