# -*- coding: utf-8 -*-

# © 2020 The Way It Should Be License
#
# Use this code in whatever manner you see fit. You can copy portions of
# the code and add it to an existing project. Or you can also import,
# statically link or dynamically link to this code.
#
# No Warranty is provided by the author
# No Liability can be placed on the author
# The author makes no Guarantees or Claims.
#
# If you break something, it's your fault!
# If the world suddenly implodes it's your fault.
# If you become a millionaire, it's your fault..(any gratuity given will
# not be turned away. :-D ).
#
# You take the good with the bad and the author takes neither.
#
# Give credit where credit is due, If copying portions of this code or copying
# it in it's entirety and using/adding it in your program the common decency rule
# applies. Add a comment line mentioning the author like the one below.
#
# "Code written by: Kevin G. Schlosser (non-responsible non-liable outside entity)"


# I wrote the framework to be used in a project I was working on.
# I didn't like the direction that project was headed and decided
# it would be best to part ways. The framework was never released
# in that projects code. It was not written to be a framework originally
# and I have been converting it into what can be used in a universal manner.
# there are still remenents in some of the files, this is because I
# have not yet finished that conversion.

# the licenses in the files DO NOT APPLY to this code base yet.
# they are a remenent and will be changed/removed if there are any still left.
# the license at the top of this file is what is to be used as a license
# for the time being.


"""
PycURL -- A Python Interface To The cURL library
================================================

PycURL is a Python interface to `libcurl`_, the multiprotocol file
transfer library. Similarly to the urllib_ Python module,
PycURL can be used to fetch objects identified by a URL from a Python program.
Beyond simple fetches however PycURL exposes most of the functionality of
libcurl, including:

- Speed - libcurl is very fast and PycURL, being a thin wrapper above
  libcurl, is very fast as well. PycURL `was benchmarked`_ to be several
  times faster than requests_.
- Features including multiple protocol support, SSL, authentication and
  proxy options. PycURL supports most of libcurl's callbacks.
- Multi_ and share_ interfaces.
- Sockets used for network operations, permitting integration of PycURL
  into the application's I/O loop (e.g., using Tornado_).

.. _was benchmarked: http://stackoverflow.com/questions/15461995/python-requests-vs-pycurl-performance
.. _requests: http://python-requests.org/
.. _Multi: https://curl.haxx.se/libcurl/c/libcurl-multi.html
.. _share: https://curl.haxx.se/libcurl/c/libcurl-share.html
.. _Tornado: http://www.tornadoweb.org/


Requirements
------------

- Python 2.7 or 3.4 through 3.6.
- libcurl 7.19.0 or better.


Installation
------------

Download source and binary distributions from `PyPI`_ or `Bintray`_.
Binary wheels are now available for 32 and 64 bit Windows versions.

Please see `the installation documentation`_ for installation instructions.

.. _PyPI: https://pypi.python.org/pypi/pycurl
.. _Bintray: https://dl.bintray.com/pycurl/pycurl/
.. _the installation documentation: http://pycurl.io/docs/latest/install.html


Documentation
-------------

Documentation for the most recent PycURL release is available on
`PycURL website <http://pycurl.io/docs/latest/>`_.


Support
-------

For support questions please use `curl-and-python mailing list`_.
`Mailing list archives`_ are available for your perusal as well.

Although not an official support venue, `Stack Overflow`_ has been
popular with some PycURL users.

Bugs can be reported `via GitHub`_. Please use GitHub only for bug
reports and direct questions to our mailing list instead.

.. _curl-and-python mailing list: http://cool.haxx.se/mailman/listinfo/curl-and-python
.. _Stack Overflow: http://stackoverflow.com/questions/tagged/pycurl
.. _Mailing list archives: https://curl.haxx.se/mail/list.cgi?list=curl-and-python
.. _via GitHub: https://github.com/pycurl/pycurl/issues


License
-------

PycURL is dual licensed under the LGPL and an MIT/X derivative license
based on the libcurl license. The complete text of the licenses is available
in COPYING-LGPL_ and COPYING-MIT_ files in the source distribution.

.. _libcurl: https://curl.haxx.se/libcurl/
.. _urllib: http://docs.python.org/library/urllib.html
.. _COPYING-LGPL: https://raw.githubusercontent.com/pycurl/pycurl/master/COPYING-LGPL
.. _COPYING-MIT: https://raw.githubusercontent.com/pycurl/pycurl/master/COPYING-MIT
"""

__PACKAGE__ = "pycurl"
__PY_PACKAGE__ = "curl"
__VERSION__ = "7.43.0.3"
__DESCRIPTION__ = 'PycURL -- A Python Interface To The cURL library'
__LONG_DESCRIPTION__ = __doc__
__AUTHOR__ = "Kjetil Jacobsen, Markus F.X.J. Oberhumer, Oleg Pudeyev"
__AUTHOR_EMAIL__ = "kjetilja@gmail.com, markus@oberhumer.com, oleg@bsdpower.com"
__MAINTAINER__ = "Oleg Pudeyev"
__MAINTAINER_EMAIL__ = "oleg@bsdpower.com"
__URL__ = "http://pycurl.io/"
__LICENSE__ = "LGPL/MIT"

from build_framework import environment

environment.setup()

from .builder import build_cares  # NOQA
from .builder import build_curl  # NOQA
from .builder import build_mbedtls  # NOQA
from .builder import build_nghttp2  # NOQA
from .builder import build_openssl  # NOQA
from .builder import build_libssh2  # NOQA
from .builder import build_zlib  # NOQA
from .builder import build_docs  # NOQA


import sys  # NOQA
import os  # NOQA

# sets distutils into a super debugging mode.
# it is easier to use a command line argument
# to turn it on.
if '--DISTUTILS_DEBUG' in sys.argv:
    os.environ['DISTUTILS_DEBUG'] = '1'
    sys.argv.remove('--DISTUTILS_DEBUG')


# this is a pip thing. I can't exactly remember
# why this causes an error but it does.
if '--no_deps' in sys.argv:
    sys.argv.remove('--no_deps')


# There is a flaw in distutils where all file copying message always take place.
# this should only be done if the verbose flag has been used in the coommand line
# this is the fix for that issue.
_verbose = '--verbose' in sys.argv

import distutils.file_util  # NOQA


_copy_file = distutils.file_util.copy_file


def copy_file(
    src,
    dst,
    preserve_mode=1,
    preserve_times=1,
    update=0,
    link=None,
    verbose=1,
    dry_run=0
):
    return _copy_file(
        src,
        dst,
        preserve_mode=preserve_mode,
        preserve_times=preserve_times,
        update=update,
        link=link,
        verbose=int(_verbose),
        dry_run=dry_run
    )


distutils.file_util.copy_file = copy_file


from setuptools import setup, find_packages  # NOQA


setup(
    name=__PACKAGE__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    long_description=__LONG_DESCRIPTION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    maintainer=__MAINTAINER__,
    maintainer_email=__MAINTAINER_EMAIL__,
    url=__URL__,
    license=__LICENSE__,
    setup_requires=build_docs.setup_requires,
    dependency_links=build_docs.dependency_links,
    cmdclass=dict(
        build_cares=build_cares.build_cares,
        build_curl=build_curl.build_curl,
        build_mbedtls=build_mbedtls.build_mbedtls,
        build_nghttp2=build_nghttp2.build_nghttp2,
        build_openssl=build_openssl.build_openssl,
        build_libssh2=build_libssh2.build_libssh2,
        build_zlib=build_zlib.build_zlib,
        build_docs=build_docs.build_docs,
    ),
    keywords=[
        'curl',
        'libcurl',
        'urllib',
        'wget',
        'download',
        'file transfer',
        'http',
        'www'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[__PY_PACKAGE__],
    package_dir={__PY_PACKAGE__: os.path.join('python', 'curl')},
)
