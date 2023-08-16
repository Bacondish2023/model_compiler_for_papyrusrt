#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import shutil
import tempfile
import logging

import model_compiler_for_papyrusrt.application as application


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'

    @unittest.skipIf(shutil.which('papyrusrt') is None, 'Papyrus-RT is not available')
    def test_typical(self):
        with tempfile.TemporaryDirectory() as tmpdir:

            # application setting
            dir_of_this_script = os.path.dirname(os.path.abspath(__file__))
            project_root_dir = os.path.dirname(os.path.dirname(dir_of_this_script)) # 2nd parent
            codegen_dir = tmpdir + os.sep + 'codegen'
            path_to_top_build_configuration = project_root_dir + os.sep + 'build_configuration' + os.sep + 'top_build_configuration.xml'

            # disable logging
            logging.basicConfig(level='WARNING')
            logging.disable(logging.CRITICAL)

            # run
            os.mkdir(codegen_dir)
            obj = application.Application(project_root_dir, codegen_dir, path_to_top_build_configuration)
            obj.main()

            # ---> verify
            self.assertTrue(os.path.isfile(codegen_dir + os.sep + 'CMakeLists.txt'))

            dir_AliceAndBob = codegen_dir + os.sep + 'AliceAndBob'
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'CMakeLists.txt'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'TopAliceAndBob.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'TopAliceAndBob.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'TopAliceAndBobControllers.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'TopAliceAndBobControllers.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'TopAliceAndBobMain.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'Alice.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'Alice.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'Bob.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'Bob.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBob + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.cc'))

            dir_libAliceAndBobProxy = codegen_dir + os.sep + 'libAliceAndBobProxy'
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'CMakeLists.txt'))
            self.assertFalse(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobProxy.hh')) # Not generated in library build
            self.assertFalse(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobProxy.cc')) # Not generated in library build
            self.assertFalse(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobProxyControllers.hh')) # Not generated in library build
            self.assertFalse(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobProxyControllers.cc')) # Not generated in library build
            self.assertFalse(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobProxyMain.cc')) # Not generated in library build
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.hh'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.cc'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AbstractAliceAndBobProxyInterface.hh'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AbstractAliceAndBobProxyInterface.cc'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyBaseInterface.hh'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyBaseInterface.cc'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyConjugateInterface.hh'))
            self.assertTrue(os.path.isfile(dir_libAliceAndBobProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyConjugateInterface.cc'))

            dir_AliceAndBobWithProxy = codegen_dir + os.sep + 'AliceAndBobWithProxy'
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'CMakeLists.txt'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobWithProxy.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobWithProxy.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobWithProxyControllers.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobWithProxyControllers.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'TopAliceAndBobWithProxyMain.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'Alice.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'Alice.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'Bob.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'Bob.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyBase.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyBase.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyConjugate.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithProxy + os.sep + 'src' + os.sep + 'AliceAndBobProxyConjugate.cc'))

            dir_AliceAndBobWithThreads = codegen_dir + os.sep + 'AliceAndBobWithThreads'
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'CMakeLists.txt'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'TopAliceAndBob.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'TopAliceAndBob.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'TopAliceAndBobControllers.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'TopAliceAndBobControllers.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'TopAliceAndBobMain.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'Alice.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'Alice.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'Bob.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'Bob.cc'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.hh'))
            self.assertTrue(os.path.isfile(dir_AliceAndBobWithThreads + os.sep + 'src' + os.sep + 'AliceAndBobProtocol.cc'))
            # <--- verify


if __name__ == '__main__':
    # executed
    unittest.main()
