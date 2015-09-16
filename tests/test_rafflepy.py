#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Eduard Trott
# @Date:   2015-09-16 15:30:33
# @Email:  etrott@redhat.com
# @Last modified by:   etrott
# @Last Modified time: 2015-09-16 16:10:59

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

    # Uploading test-spreadsheet
    d2g.upload(df_upload, filepath)
    credentials = get_credentials()
    file_id = get_file_id(credentials, filepath)

    # loading via file_id
    uri = file_id
    pool = raffle.input_gload(uri)

    assert all(pool == df_upload['Username'].values)

    # loading certain column
    column = 'color'
    pool = raffle.input_gload(uri, column)

    assert all(pool == df_upload['color'].values)

    # Clear created file from drive
    delete_file(credentials, file_id)
