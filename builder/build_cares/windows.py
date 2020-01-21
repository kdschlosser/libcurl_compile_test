
from build_framework import PLATFORM
from ..sources import CARES_SOURCES
from ..dep_versions import CARES_VERSION

import build_framework.library.windows


MACROS = [
    ('_WINDOWS', '1'),
    ('_UNICODE', '1'),
    ('UNICODE', '1'),
    ('CARES_BUILDING_LIBRARY', '1'),
    ('CARES_STATICLIB', '1'),
    ('_VC80_UPGRADE', '0x0600')
]

LIBS = []
LIB_DIRS = []
UDEF_MACROS = []
CFLAGS = []
LDFLAGS = []

INCLUDES = ["."]

if PLATFORM == 'x64':
    MACROS += [
        ('ssize_t', 'long')
    ]


class Library(build_framework.library.windows.Library):

    def __init__(self):
        name = 'cares'
        sources = CARES_SOURCES
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
        version = CARES_VERSION

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
