
from build_framework import DEBUG, PLATFORM

MACROS = [
    ('_WINDOWS', '1'),
    ('_USRDLL', '1'),
    ('_UNICODE', '1'),
    ('UNICODE', '1'),
    ('MBEDTLS_EXPORTS', '1')
]

UNDEF_MACROS = []
CFLAGS = [
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
    '/Fp"Release/mbedtls.pch"',
    '/diagnostics:column'
]
LDFLAGS = ['/OUT:"Release/nmbedTLS.lib"', '/NOLOGO']


INCLUDES = [
    "include"
    "crypto/include"
    "crypto/3rdparty/everest/include/"
    "crypto/3rdparty/everest/include/everest"
    "crypto/3rdparty/everest/include/everest/vs2010"
    "crypto/3rdparty/everest/include/everest/kremlib"
]



if DEBUG:
    MACROS += [('_DEBUG', '1')]
    CFLAGS += [
        '/JMC',
        '/TC',
        '/Yu"pch.h"',
        '/ZI',
        '/Od',
        '/Fd"Release/mbedTLS.pdb"',
        '/RTC1',
        '/MDd'
    ]
else:
    MACROS += [('NDEBUG', '1')]
    CFLAGS += [
        '/GL',
        '/Gy',
        '/Zi',
        '/O2',
        '/Oi',
        '/MD'
    ]
    LDFLAGS += ['/LTCG']


if PLATFORM == 'x86':
    MACROS += [('WIN32', '1')]
    CFLAGS += ['/analyze-']

    if DEBUG:
        MACROS += ['/Oy-']

    LDFLAGS += ['/MACHINE:X86']

else:
    MACROS += [('WIN64', '1'), ('ssize_t', 'long')]
    LDFLAGS += ['/MACHINE:X64']
