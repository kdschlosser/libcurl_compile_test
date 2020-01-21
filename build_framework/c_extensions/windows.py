# -*- coding: utf-8 -*-

from __future__ import print_function
from . import extension_base
from msvc import environment


class Extension(extension_base.Extension):

    def __init__(
        self,
        name,
        sources,
        include_dirs=None,
        define_macros=None,
        undef_macros=None,
        library_dirs=None,
        libraries=None,
        runtime_library_dirs=None,
        extra_objects=None,
        extra_compile_args=None,
        extra_link_args=None,
        export_symbols=None,
        swig_opts=None,
        depends=None,
        language=None,
        optional=None,
        **kw  # To catch unknown keywords
    ):

        if extra_link_args is None:
            extra_link_args = ['/debug:full']

        if extra_compile_args is None:
            extra_compile_args = [
                '/FS',
                # Enables function-level linking.
                '/Gy',
                # Creates fast code.
                '/O2',
                # Uses the __cdecl calling convention (x86 only).
                '/Gd',
                # Omits frame pointer (x86 only).
                '/Oy',
                # Generates intrinsic functions.
                '/Oi',
                # generate pdb file for debugging.
                '/Zi',
                '/Ox',
                '/fp:precise',
                # Specifies standard behavior
                '/Zc:wchar_t',
                # Specifies standard behavior
                '/Zc:forScope',
                # I cannot remember what this does. I do know it does get rid of
                # a compiler warning
                '/EHsc',
                # compiler warnings to ignore
                '/wd4996',
                '/wd4244',
                '/wd4005',
                '/wd4800',
                '/wd4351',
                '/wd4273'
            ]

            if environment.visual_c.version > 10.0:
                # these compiler flags are not valid on
                # Visual C++ version 10.0 and older

                extra_compile_args += [
                    # Forces writes to the program database (PDB) file to be
                    # serialized through MSPDBSRV.EXE.
                    '/FS',
                    # Specifies standard behavior
                    '/Zc:inline'
                ]

        if libraries is None:
            libraries = [environment.python.dependency.split('.')[0]]

        extension_base.Extension.__init__(
            self,
            name,
            sources,
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
            swig_opts=swig_opts,
            depends=depends,
            language=language,
            optional=optional,
            **kw
        )
