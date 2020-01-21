
# linux only LIBSSH2_LIBGCRYPT
from build_framework import DEBUG, PLATFORM
import os

from ..sources import LIBSSH2_SOURCES
from ..dep_versions import SSH2_VERSION

import build_framework.library.windows

LIBSSH2_SOURCES += ['src/wincng.c']

MACROS = [
    ('LIBSSH2_WINCNG', '1'),
    ('_WINDOWS', '1'),
    ('_LIB', '1'),
    ('_UNICODE', '1'),
    ('UNICODE', '1')
]

UDEF_MACROS = ['BUILD_SHARED_LIBS', 'BUILD_TESTING', 'BUILD_EXAMPLES']

CFLAGS = [
    '/Zc:inline',
    '/Zc:forScope',
]
LDFLAGS = []

INCLUDES = ['include', 'win32']
LIBS = ['ws2_32.lib', 'user32.lib', 'advapi32.lib', 'gdi32.lib']
LIB_DIRS = []


class Library(build_framework.library.windows.Library):

    def _compile_c(self, c_file, build_clib):

        ssl_path = os.path.join(build_clib.build_temp, 'openssl')
        if os.path.exists(ssl_path):
            if ('LIBSSH2_OPENSSL', '1') not in self._define_macros:
                self._define_macros += [('LIBSSH2_OPENSSL', '1')]
            if ssl_path not in self._include_dirs:
                self._include_dirs += [ssl_path]

            if 'libeay32.lib' not in self._libraries:
                self._libraries += ['libeay32.lib']

            if 'ssleay32.lib' not in self._libraries:
                self._libraries += ['ssleay32.lib']

            if ssl_path not in self._library_dirs:
                self._library_dirs += [ssl_path]

            if 'src/openssl.c' not in self._sources:
                self._sources += ['src/openssl.c']

        mbedtls_path = os.path.join(build_clib.build_temp, 'mbedtls')
        if os.path.exists(mbedtls_path):

            if ('LIBSSH2_MBEDTLS', '1') not in self._define_macros:
                self._define_macros += [('LIBSSH2_MBEDTLS', '1')]
            if mbedtls_path not in self._include_dirs:
                self._include_dirs += [mbedtls_path]

            if 'mbedtls.lib' not in self._libraries:
                self._libraries += ['mbedtls.lib']

            if mbedtls_path not in self._library_dirs:
                self._library_dirs += [mbedtls_path]

            if 'src/mbedtls.c' not in self._sources:
                self._sources += ['src/mbedtls.c']

        build_framework.library.windows.Library._compile_c(self, c_file, build_clib)

    def __init__(self):
        name = 'libssh2'
        sources = LIBSSH2_SOURCES
        include_dirs = INCLUDES
        define_macros = MACROS
        undef_macros = UDEF_MACROS
        library_dirs = LIB_DIRS
        libraries = LIBS
        runtime_library_dirs = ()
        extra_objects = ()
        extra_compile_args = CFLAGS
        extra_link_args = LDFLAGS
        export_symbols = ()
        depends = ()
        static_lib = True
        version = SSH2_VERSION

        build_framework.library.windows.Library.__init__(
            self,
            name=name,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            undef_macros=undef_macros,
            library_dirs=library_dirs,
            libraries=libraries,
            runtime_library_dirs=runtime_library_dirs,
            extra_objects=extra_objects,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            export_symbols=export_symbols,
            depends=depends,
            static_lib=static_lib,
            version=version,
        )

        # this enables the use of the build_framework multi threaded compiler
        self.build = self._build


