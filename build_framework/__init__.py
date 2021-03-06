# -*- coding: utf-8 -*-

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

import sys
import zipfile
import io
import os
import distutils.log
import ctypes


if ctypes.sizeof(ctypes.c_void_p) == 8:
    PLATFORM = 'x64'
else:
    PLATFORM = 'x86'

DEBUG = os.path.splitext(sys.executable)[0].endswith('d')


def get_dep(path, url):
    """download an archive to a specific location"""
    try:
        distutils.log.info(
            "fetching {0} to {1}".format(
                url,
                path,
            )
        )

        response = urlopen(url)

        dst_file = io.BytesIO(response.read())
        dst_file.seek(0)
        zip_ref = zipfile.ZipFile(dst_file)
        dst = os.path.split(path)[0]
        zip_ref.extractall(dst)
        zip_ref.close()
        dst_file.close()

        dst = os.path.join(dst, zip_ref.namelist()[0])

        if dst != path:
            os.rename(dst, path)

        return True
    except:
        import traceback
        distutils.log.error(traceback.format_exc())
        return False
