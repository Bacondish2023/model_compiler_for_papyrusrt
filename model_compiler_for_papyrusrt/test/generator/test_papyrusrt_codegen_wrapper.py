#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import tempfile

import model_compiler_for_papyrusrt.generator.papyrusrt_codegen_wrapper as papyrusrt_codegen_wrapper


class TestPapyrusrtCodegenWrapperStub(unittest.TestCase):

    def test_typical(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            obj = papyrusrt_codegen_wrapper.PapyrusrtCodegenWrapperStub(
                '', # Stub does not care
                '', # Stub does not care
                )

            obj.generate(
                '',     # Stub does not care
                'Top',
                tmpdir,
                'OFF',  # Stub does not care
                False,  # Stub does not care
            )

            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'TopMain.cc'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'TopControllers.hh'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'TopControllers.cc'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Top.hh'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Top.cc'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Foo.hh'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Foo.cc'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Bar.hh'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'CMakeLists.txt'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Makefile'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'MakefileTop.mk'))
            self.assertEqual(True, os.path.isfile(tmpdir + os.sep + 'src' + os.sep + 'Top-connections.log'))


if __name__ == '__main__':
    # executed
    unittest.main()
