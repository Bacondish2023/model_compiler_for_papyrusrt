#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import logging
import tempfile

import model_compiler_for_papyrusrt.generator.target_specific_generator as target_specific_generator
import model_compiler_for_papyrusrt.build_configuration.build_configuration as build_configuration


class TestTargetSpecificGenerator(unittest.TestCase):
    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'


    def test_typical_executable_foo(self):
        bc = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_foo.xml')
        with tempfile.TemporaryDirectory() as tmpdir:
            codegen_dir = tmpdir + os.sep + 'codegen'
            obj = target_specific_generator.TargetSpecificGenerator(
                bc,
                tmpdir,         # Stub does not care
                codegen_dir,
                tmpdir,         # Stub does not care
                True,           # Specify stub generator
            )

            obj._codegen_with_papyrusrt()
            open(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.hh', 'w').close() # Create unnecessary file
            open(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.cc', 'w').close() # Create unnecessary file

            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopMain.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopControllers.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopControllers.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Foo.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Foo.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Bar.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.hh'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.cc'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'CMakeLists.txt'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Makefile'))         # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'MakefileTop.mk'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top-connections.log'))
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'CMakeLists.txt'))

            obj._arrange_codegen_dir()
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopMain.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopControllers.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'TopControllers.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Foo.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Foo.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Bar.hh'))
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.hh'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Baz.cc'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'CMakeLists.txt'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Makefile'))        # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'MakefileTop.mk'))  # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'src' + os.sep + 'Top-connections.log'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'CMakeLists.txt'))


    def test_typical_library_foo(self):
        bc = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_library_foo.xml')
        with tempfile.TemporaryDirectory() as tmpdir:
            codegen_dir = tmpdir + os.sep + 'codegen'
            obj = target_specific_generator.TargetSpecificGenerator(
                bc,
                tmpdir,         # Stub does not care
                codegen_dir,
                tmpdir,         # Stub does not care
                True,           # Specify stub generator
            )

            obj._codegen_with_papyrusrt()
            open(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.hh', 'w').close() # Create unnecessary file
            open(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.cc', 'w').close() # Create unnecessary file

            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopMain.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopControllers.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopControllers.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Foo.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Foo.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Bar.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.hh'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.cc'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'CMakeLists.txt'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Makefile'))         # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'MakefileTop.mk'))   # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top-connections.log'))
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'CMakeLists.txt'))

            obj._arrange_codegen_dir()
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopMain.cc'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopControllers.hh'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'TopControllers.cc'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top.hh'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top.cc'))  # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Foo.hh'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Foo.cc'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Bar.hh'))
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.hh'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Baz.cc'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'CMakeLists.txt'))  # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Makefile'))        # unnecessary
            self.assertEqual(False, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'MakefileTop.mk'))  # unnecessary
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'src' + os.sep + 'Top-connections.log'))
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'libFoo' + os.sep + 'CMakeLists.txt'))


    def test_controllers_file_typical(self):
        bc = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_foo.xml')
        with tempfile.TemporaryDirectory() as tmpdir:
            codegen_dir = tmpdir + os.sep + 'codegen'
            model_dir = tmpdir + os.sep + 'model'

            os.makedirs(model_dir)

            obj = target_specific_generator.TargetSpecificGenerator(
                bc,
                tmpdir,         # Stub does not care
                codegen_dir,
                tmpdir,         # Stub does not care
                True,           # Specify stub generator
            )

            obj._generate()
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'Top.controllers'))


    def test_controllers_file_overwrite(self):
        # supsress logging because this test cause warning logging
        logging.basicConfig(level='WARNING')
        logging.disable(logging.CRITICAL)

        bc = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_foo.xml')
        with tempfile.TemporaryDirectory() as tmpdir:
            codegen_dir = tmpdir + os.sep + 'codegen'
            model_dir = tmpdir + os.sep + 'model'

            os.makedirs(model_dir)
            open(model_dir + os.sep + 'Top.controllers', 'w').close() # controllers file already exists

            obj = target_specific_generator.TargetSpecificGenerator(
                bc,
                tmpdir,         # Stub does not care
                codegen_dir,
                tmpdir,         # Stub does not care
                True,           # Specify stub generator
            )

            obj._generate()
            self.assertEqual(True, os.path.isfile(codegen_dir + os.sep + 'Foo' + os.sep + 'Top.controllers'))


if __name__ == '__main__':
    # executed
    unittest.main()
