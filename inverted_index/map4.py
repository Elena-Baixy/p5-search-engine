#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys

for line in sys.stdin:
    print (f"{line.split()[0]} {line.split()[1]} \t {line.split()[2]} {line.split()[3]} {line.split()[4]}")

