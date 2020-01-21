# -*- coding: utf-8 -*-

from .. import build_clib
from ..dep_versions import OPENSSL_VERSION


URL = 'https://github.com/openssl/openssl'
DOWNLOAD_URL = URL + '/archive/OpenSSL_{0}.zip'
VERSION = OPENSSL_VERSION


# I know this seems kind of odd... I am doing a tiny bit of voodoo magic code here
# I need the class name in order to set up the directories
# and i use the __module__ attribute of the class in order to get this module instance
# from sys.modules. I use that module instance to grab the 3 constants in this file.
class build_openssl(build_clib.build_clib):
    pass

