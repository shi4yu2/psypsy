#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
A modified version of Christophe Pallier's Shuffle

Shuffles lines from a table with optional constraints on repetitions.

Constraints:
max_rep: maximum number of repetitions of a string in a columns
min_gap: minimum distances (in rows) between two repetitions of a string
(maxrep and mingat are dictionaries mapping column number
to a number expressing the constraint)
"""

__author__ = 'ShY'
__copyright__ = 'Copyright 2018, SHY'
__version__ = '0.1.0 (20180530)'
__maintainer__ = 'ShY, Pierre Halle'
__email__ = 'shi4yu2@gmail.com'
__status__ = 'Development'


import csv
import random
import time


def read_csv(filename):
    # type: (str) -> tuple[list, list]
    """
    Read CSV files and return a list of lists
    :param filename: filename
    :type filename: str
    :return: list of lists of str, list of header
    :rtype: tuple
    """
    try:
        with open(filename, 'r') as csv_file:
            dialect = csv.Sniffer().sniff(csv_file.readline(), [',', ';', '\t', ' '])
            csv_file.seek(0)
            data_frame = csv.reader(csv_file, dialect)
            output_list = []
            for row_i in data_frame:
                output_list.append(row_i)
            header = output_list.pop(0)
            return output_list, header
    except OSError:
        print("File not found")


def swap(table, row_i, row_j):
    # type: (list, int, int) -> list
    """
    swap two elements of a list
    :param table: list to modify
    :type table: list
    :param row_i: row number i
    :type row_i: int
    :param row_j: row number j
    :type row_j: int
    :return: table: the same list after swap
    :rtype: table: list
    """
    tmp = table[row_i]
    table[row_i] = table[row_j]
    table[row_j] = tmp
    return table


def shuffle_eq_prob(table, max_rep=None, min_gap=None, time_limit=1):
    # type: (list, dict, dict, int) -> list
    """
    Make a large number of randomisation to reach the eq-probability
    :param table: table of conditions
    :type table: list[list[str]]
    :param max_rep: maximum number of repetitions of a string in a columns
    :type max_rep: dict
    :param min_gap: minimum distances (in rows) between two repetitions of a string
    in the same column
    :type min_gap: dict
    :param time_limit: max time in second of execution
    :type time_limit: int
    :return: table after randomisation
    :rtype: list[list[str]]
    """
    start_time = time.time()
    continue_shuffle = True  # test if table respect all constraints
    test = True  # return bool value of constraints check

    while continue_shuffle and (time.time() < (start_time + time_limit)):
        random.shuffle(table)  # Randomise lines in table
        test, _ = check_constraints(table, max_rep, min_gap)
        continue_shuffle = not test  # end condition for while
    if not test:
        return []
    else:
        return table


def check_constraints(table, max_rep=None, min_gap=None, row_i=0):
    # type: (list, dict, dict, int) -> (bool, int)
    """
    Checks if a permutation respects constraints.
    :param table: input list
    :type table: list
    :param max_rep: maximum number of repetitions of a string in a columns
    :type max_rep: dict
    :param min_gap: minimum distances (in rows) between two repetitions of a string
    :type min_gap: dict
    :param row_i: selected line
    :type row_i: int
    :return: tuple of test and row number
    :rtype: tuple(bool, int)
    """
    if max_rep is not None:
        repetitions = max_rep.copy()  # make a copy of max repetition constraints
        for field in repetitions.keys():
            repetitions[field] = 1

    if row_i < 0:
        row_i = 0

    previous_line = table[row_i]  # get selected line of table
    row_i += 1
    da = True

    while da and row_i < len(table):
        line = table[row_i]

        # check max_rep constraints ===========================================
        if max_rep is not None:
            for field in max_rep.keys():
                if previous_line[field] == line[field]:
                    # test if condition for line & pre-line are the same
                    repetitions[field] += 1
                    da = (repetitions[field] <= max_rep[field])
                else:
                    repetitions[field] = 1
                if not da:
                    break

        # check min_gap constraints ===========================================
        if min_gap is not None:
            for field in min_gap.keys():
                previous_col = row_i - min_gap[field]
                if previous_col < 0:
                    previous_col = 0

                while da and (previous_col < row_i):
                    da = da and (table[previous_col][field] != table[row_i][field])
                    previous_col += 1
                if not da:
                    break

        previous_line = line

        if da:
            row_i += 1

    return da, row_i


def randomise_stimuli(table, max_rep=None, min_gap=None, time_limit=1):
    """
    Shuffle the condition table
    :param table: table of conditions
    :type table: list[list[str]]
    :param max_rep: maximum number of repetitions of a string in a columns
    :type max_rep: dict
    :param min_gap: minimum distances (in rows) between two repetitions of a string
    :type min_gap: dict
    :param time_limit: max time in second of execution
    :type time_limit: int
    :return table: table after randomisation
    :rtype table: list[list[str]]
    """
    n = len(table)  # get length of the table

    m1, m2 = 0, 0
    if min_gap is not None:
        m1 = max(min_gap.values())
    if max_rep is not None:
        m2 = max(max_rep.values())

    backtrack = max(m1, m2)

    start_time = time.time()
    random.shuffle(table)

    da = False
    row_i = 0
    n_failure = 0

    while not da and (time.time() < (start_time + time_limit)):
        da, row_i = check_constraints(table, max_rep, min_gap, row_i - backtrack)

        if not da:
            n_failure += 1
            if (row_i >= (n - 1)) or (n_failure > (n * 100)):  # start again
                # Reinitialise all, redo randomisation
                random.shuffle(table)
                row_i = 0
                n_failure = 0
            else:  # swap current row with another one further down the table
                row_j = random.choice(range(row_i + 1, n))
                swap(table, row_i, row_j)

    if da:
        return table
    else:
        return []


