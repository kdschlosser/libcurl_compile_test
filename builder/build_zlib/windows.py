
from ..sources import ZLIB_SOURCES
from ..dep_versions import ZLIB_VERSION
import build_framework.library.windows

MACROS = [
    ('_WINDOWS', '1'),
    ('_CRT_SECURE_NO_DEPRECATE', '1'),
    ('_CRT_NONSTDC_NO_DEPRECATE', '1')
]
INCLUDES = []
UDEF_MACROS = []
LIB_DIRS = []
LIBS = []
CFLAGS = []
LDFLAGS = []


class Library(build_framework.library.windows.Library):

    def __init__(self):
        name = 'zlib'
        sources = ZLIB_SOURCES
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
        version = ZLIB_VERSION

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


