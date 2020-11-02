#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import string
import sys

MYFILE=sys.argv[1]

with open(str(MYFILE), 'r', newline='', encoding='cp437') as f:
	for row in csv.reader(f, skipinitialspace=True):
		row = [col.strip() for col in row]
		print(",".join(map(str, row)))