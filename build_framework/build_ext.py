# -*- coding: utf-8 -*-

import sys
import setuptools.command.build_ext
import distutils.log
import os
import shutil

PY3 = sys.version_info[0] > 2


class build_ext(setuptools.command.build_ext.build_ext):

    def has_c_libraries(self):
        return False

    def finalize_options(self):
        build = self.distribution.get_command_obj('build')
        build.ensure_finalized()

        self.distribution.has_c_libraries = self.has_c_libraries

        self.static = build.static
        self.saved_libtype = setuptools.command.build_ext.libtype
        self.saved_use_stubs = setuptools.command.build_ext.use_stubs

        if self.static:
            self.link_shared_object = self.static_object
            setuptools.command.build_ext.libtype = 'static'
            setuptools.command.build_ext.use_stubs = False
        else:
            self.link_shared_object = self.shared_object
            setuptools.command.build_ext.libtype = 'shared'
            setuptools.command.build_ext.use_stubs = True

        extension = self.distribution.ext_modules[0]

        build_clib = self.distribution.get_command_obj('build_clib')
        build_clib.ensure_finalized()

        extension(self)

        self.init_extensions = []

        for ext in self.distribution.ext_modules[1:]:
            if '__init__' in ext.name or 'command_classes' in ext.name:
                self.distribution.ext_modules.remove(ext)
                self.init_extensions += [ext]

    def run(self):
        if self.init_extensions:
            distutils.log.info('\n')
            for ext in self.init_extensions:
                self.build_extension(ext)

            distutils.log.info('\n')

        setuptools.command.build_ext.build_ext.run(self)

        # TODO: write code parser for building a stub file
        # a stub file is used to provide a "peek" inside of an en extension. This is what allows
        # an IDE to provide type hinting and intellisense.
        # Python 2.x does not have support for .pyi files. But I know a way to provide the same
        # ability without the need to use a .pyi file.

        # self.run_command('build_stub')

    def get_ext_fullpath(self, name):
        # this method is overridden because of Windows and needing to compile an extension with the same
        # version compiler that was used to compile Python. When building a wheel or an egg
        # we are able to create that binary for each of the Python versions that use a specific msvc compiler
        # an example would be 3.5, 3.6, 3.7, 3.8  all use msvc 14. because the naming conventions of the pyd file
        # target specific python versions like this "kiwisolver.cp37-win_amd64.pyd" we need to shop out all
        # of the middle bits to end up with "kiwisolver.pyd". this file name for the extension is still able
        # to be loaded by python. and this is what gets packaged into the wheel. so we are able to build
        # 4 wheels or 4 eggs with only having to run the build for one of the python versions listed above.
        # the wheel/egg filename is what is going to set the python version/archeticture the wheel/egg is
        # allowed to be installed on.

        path = setuptools.command.build_ext.build_ext.get_ext_fullpath(
            self,
            name
        )

        path, file_name = os.path.split(path)

        if PY3:
            file_name = file_name.split('.')
            file_name = '.'.join([file_name[0], file_name[-1]])

        return os.path.join(path, file_name)

    def build_extension(self, ext):
        ext_path = self.get_ext_fullpath(ext.name)
        pdb_file = os.path.splitext(ext_path)[0] + '.pdb'

        if '__init__' in ext.name or 'command_classes' in ext.name:
            src = os.path.splitext(ext.sources[0])[0] + '.pyx'
            dst = os.path.splitext(ext_path)[0] + '.py'
            output_path = os.path.split(dst)[0]

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            distutils.log.info(
                'copying {0}  -->  {1}...'.format(
                    os.path.relpath(src),
                    os.path.relpath(dst)
                )
            )

            shutil.copy(src, dst)
        else:
            if ext.name != 'libopenzwave':
                try:
                    delattr(self, 'link_shared_object')
                    setuptools.command.build_ext.libtype = self.saved_libtype
                    setuptools.command.build_ext.use_stubs = self.saved_use_stubs
                except AttributeError:
                    pass

            if 'bdist_wheel' in sys.argv:
                if not os.path.exists(ext_path):
                    setuptools.command.build_ext.build_ext.build_extension(self, ext)
                    distutils.log.info('\n')
            else:
                setuptools.command.build_ext.build_ext.build_extension(self, ext)
                distutils.log.info('\n')

            if not sys.platform.startswith('win'):
                from subprocess import Popen, PIPE

                proc = Popen(['objcopy', '--only-keep-debug', ext_path, pdb_file], stdout=PIPE, stderr=PIPE)
                proc.communicate()

                proc = Popen(['objcopy', '--strip-debug', ext_path], stdout=PIPE, stderr=PIPE)
                proc.communicate()

                proc = Popen(['objcopy', '--add-gnu-debuglink', pdb_file, ext_path], stdout=PIPE, stderr=PIPE)
                proc.communicate()

    def shared_object(
        self,
        objects,
        output_libname,
        output_dir=None,
        libraries=None,
        library_dirs=None,
        runtime_library_dirs=None,
        export_symbols=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None
    ):
        self.link(
            self.SHARED_LIBRARY,
            objects,
            output_libname,
            output_dir,
            libraries,
            library_dirs,
            runtime_library_dirs,
            export_symbols,
            debug,
            extra_preargs,
            extra_postargs,
            build_temp,
            target_lang
        )

    def static_object(
        self,
        objects,
        output_libname,
        output_dir=None,
        libraries=None,
        library_dirs=None,
        runtime_library_dirs=None,
        export_symbols=None,
        debug=0,
        extra_preargs=None,
        extra_postargs=None,
        build_temp=None,
        target_lang=None
    ):
        # XXX we need to either disallow these attrs on Library instances,
        # or warn/abort here if set, or something...
        # libraries=None, library_dirs=None, runtime_library_dirs=None,
        # export_symbols=None, extra_preargs=None, extra_postargs=None,
        # build_temp=None

        assert output_dir is None  # distutils build_ext doesn't pass this
        output_dir, filename = os.path.split(output_libname)
        basename, ext = os.path.splitext(filename)
        if self.library_filename("x").startswith('lib'):
            # strip 'lib' prefix; this is kludgy if some platform uses
            # a different prefix
            basename = basename[3:]

        self.create_static_lib(
            objects,
            basename,
            output_dir,
            debug,
            target_lang
        )
