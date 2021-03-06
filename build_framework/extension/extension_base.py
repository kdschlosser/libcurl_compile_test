# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import distutils.log
import setuptools.extension


class Extension(setuptools.extension.Extension):
    # right now you use a dictionary in which you add the various information
    # to. and this is very hard to follow. in the end you then pass the
    # dictionary to the parent class of this class. You can trim down on the
    # hard to follow dictionary use and simply place the code that pertains
    # to a specific OS into a subclass of this class and just pass an instance
    # of that class directly to setup() this works pretty much the same as
    # the Library class. you would add a subclass of this class and a subclass
    # of the Library class to a file that is specific to that OS.

    def report_config(self):
        pass

    def has_c_libraries(self):
        return False

    def __call__(self, build_ext):
        builder = build_ext.distribution.get_command_obj('build')
        builder.ensure_finalized()

        self.openzwave = openzwave = builder.openzwave
        self.flavor = flavor = builder.flavor
        self.static = static = builder.static
        self.backend = backend = builder.backend

        self.define_macros += [
            ('PY_LIB_FLAVOR', flavor),
            ('PY_LIB_BACKEND', backend)
        ]

        if backend == 'cython':
            self.define_macros += [
                ('CYTHON_FAST_PYCCALL', 1),
                ('PY_SSIZE_T_CLEAN', 1)
            ]
            self.sources += [
                'src-lib/libopenzwave/libopenzwave.pyx'
            ]

        elif backend == 'cpp':
            self.define_macros += [('PY_SSIZE_T_CLEAN', 1)]
            self.sources += [
                os.path.join(
                    openzwave,
                    'python-openzwave',
                    'src-lib',
                    'libopenzwave',
                    'libopenzwave.cpp'
                )
            ]
            self.include_dirs += [
                'src-lib/libopenzwave'
            ]

        cpp_path = os.path.join(openzwave, 'cpp')
        src_path = os.path.join(cpp_path, 'src')

        if static:
            self.include_dirs += [
                src_path,
                os.path.join(src_path, 'value_classes'),
                os.path.join(src_path, 'platform')
            ]

    def __init__(
        self,
        extra_objects,
        sources,
        include_dirs,
        define_macros,
        libraries,
        extra_compile_args,
        extra_link_args=[],
        undef_macros=[],
        library_dirs=[],
        runtime_library_dirs=[],
        export_symbols=[],
        swig_opts=[],
    ):
        self.openzwave = ''
        self.static = None
        self.flavor = ''
        self.backend = ''
        self.build_path = ''

        # if you look at the contents of the method you will see that it
        # sets all of the various build settings that are common to all of
        # the OS's it also handles the backend type being cpp or cython. I
        # know there was code added for pybind i have not been able to
        # locate where it is actually used.
        name = 'libopenzwave'
        language = 'c++'

        define_macros += [
            ('PY_LIB_VERSION', pyozw_version.pyozw_version),
            ('_MT', 1),
            ('_DLL', 1)
        ]

        setuptools.extension.Extension.__init__(
            self,
            name=name,
            language=language,
            extra_objects=extra_objects,
            sources=sources,
            include_dirs=include_dirs,
            define_macros=define_macros,
            libraries=libraries,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
            undef_macros=undef_macros,
            library_dirs=library_dirs,
            runtime_library_dirs=runtime_library_dirs,
            export_symbols=export_symbols,
            swig_opts=swig_opts
        )

        # this is a nasty hack because Cython uses the __class__ of the
        # instance passed to it to create a new extension
        def __new__init__(*args, **kwargs):
            setuptools.extension.Extension.__init__(*args, **kwargs)

        self.__class__.__init__ = __new__init__

