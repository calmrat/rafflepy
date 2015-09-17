#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-17 11:41:28
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-17 11:42:44


from __future__ import unicode_literals, absolute_import

from instructions import commands, datatypes
import pytest

TEST_REPO = 'kejbaly2/rafflepy'


def test_global_import():
    import rafflepy


@pytest.mark.xfail(reason="Credentials")
def test_gspread_load():
    import random
    import string

    import pandas as pd
    from df2gspread import df2gspread as d2g
    from df2gspread import gspread2df as g2d
    from df2gspread.utils import get_credentials
    from df2gspread.gfiles import get_file_id
    from df2gspread.gfiles import delete_file

    from rafflepy import raffle

    df_upload = pd.DataFrame({'color': ['b', 'w', 'p', 'm'],
                              'Username': ['John', 'Nicolos', 'Katy', 'Mike'],
                              'Other': [1, 2, 3, 4]})

    filepath = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    # Uploading df to test-spreadsheet
    d2g.upload(df_upload, filepath)
    credentials = get_credentials()
    file_id = get_file_id(credentials, filepath)

    # Downloading via file_id
    uri = file_id
    pool = raffle.input_gload(uri)

    assert all(pool == df_upload['Username'].values)

    # Downloading certain column
    column = 'color'
    pool = raffle.input_gload(uri, column)

    assert all(pool == df_upload['color'].values)

    # Clear created file from drive
    delete_file(credentials, file_id)


def test_csv_load():
    import os

    import pandas as pd

    from rafflepy import raffle

    df_upload = pd.DataFrame({'color': ['b', 'w', 'p', 'm'],
                              'Username': ['John', 'Nicolos', 'Katy', 'Mike'],
                              'Other': [1, 2, 3, 4]})

    uri = 'sample.csv'

    # Uploading df to csv
    df_upload.to_csv(uri, encoding='utf-8')

    # Downloading with default column
    pool = raffle.input_load(uri)

    assert all(pool == df_upload['Username'].values)

    # Downloading certain column
    column = 'color'
    pool = raffle.input_load(uri, column)

    assert all(pool == df_upload['color'].values)

    # Clear created file
    os.remove(uri)


@pytest.mark.parametrize('execution_number', range(10))
def test_exclude(execution_number):
    import string
    import random

    from rafflepy import raffle

    pool = [''.join([random.choice(string.ascii_uppercase + string.digits)
                     for _ in range(random.randint(2, 10))])
            for _ in range(random.randint(2, 10))]
    exclude = [random.choice(range(0, len(pool)))
               for _ in range(random.randint(1, len(pool)))]
    assert set(pool) - set(exclude) == raffle.input_filter(pool, exclude)
