from build_framework import PLATFORM
from ..sources import NGHTTP2_SOURCES
from ..dep_versions import NGHTTP2_VERSION
import build_framework.library.windows


MACROS = [
    ('_WINDOWS', '1'),
    ('_LIB', '1'),
    ('_UNICODE', '1'),
    ('UNICODE', '1'),
    ('ENABLE_LIB_ONLY', '1'),
    ('NGHTTP2_STATICLIB', '1')
]

LIBS = []
LIB_DIRS = []
UDEF_MACROS = ["ENABLE_ASIO_LIB"]
CFLAGS = [
    '/permissive-',
    '/GS',
    '/W3',
    '/Zc:wchar_t',
    '/Gm-',
    '/sdl',
    '/Zc:inline',
    '/fp:precise',
    '/errorReport:prompt',
    '/WX-',
    '/Zc:forScope',
    '/Gd',
    '/FC',
    '/Fa"Release/"',
    '/EHsc',
    '/nologo',
    '/Fo"Release/"',
    '/Fp"Release/nghttp2.pch"',
    '/diagnostics:column'
]
LDFLAGS = []

INCLUDES = ['includes']


if PLATFORM == 'x64':
    MACROS += [('ssize_t', 'long')]


class Library(build_framework.library.windows.Library):

    def __init__(self):
        name = 'nghttp2'
        sources = NGHTTP2_SOURCES
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
        version = NGHTTP2_VERSION

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


