#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configure randomisation constraints
"""

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180530)'
__maintainer__ = 'ShY, Pierre Halle'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'


import libpsypsy.psypsyio as psypsyio
import libpsypsy.psypsyrandom as psypsyrandom

# Usage:
# =======================
# 0. All input files should have a header
# 1. Replace file name and constraints by your file and constraints
# 2. python3 randomisation_config.py
# 3. Get your constraint in "constraints.txt"


# Replace filename by the input filename
filename = "axb_00.txt"
# Example: filename = "axb_00.txt"

_, stimuli_header = psypsyio.read_csv(filename)
print(stimuli_header)

# Replace head dictionary content by wished constraints
constraints = {"consonant": 2, "position": 2}
# Example: constraints = {"consonant": 2, "position": 2}

result = psypsyrandom.make_constraints(stimuli_header, constraints)
result_file = open("constraints.txt", 'w')
print("constraints = " + str(result), file=result_file)
# constraint dictionary is in the file "constraints.txt", copy-paste to your code
