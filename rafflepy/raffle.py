#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   raffle - Easily select a winner!
#   Author: Chris Ward <kejbaly2@gmail.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2015 Chris Ward. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
Quickly select a random set of winners from a pool of candidates.
"""

from __future__ import unicode_literals, absolute_import

import csv
import os
import re
from df2gspread import gspread2df

is_local_file = re.compile('^(file://)?(\/?.+)$')


def input_gload(uri, column='Username', wks_name=None):
    df = gspread2df.download(uri, wks_name, col_names=True)
    pool = df[column]
    return pool.values


def input_load(uri, column='Username'):
    uri = os.path.expanduser(uri)
    protocol, uri = is_local_file.match(uri).groups()
    if not protocol:
        f = open(uri)
        pool = [r[column] for r in csv.DictReader(f)]
    else:
        raise RuntimeError
    return pool


def input_filter(pool, exclude):
    pool = set(pool or [])
    exclude = set(exclude or [])
    return pool - exclude
