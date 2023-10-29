#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import xml.etree.ElementTree

import model_compiler_for_papyrusrt.build_configuration.top_build_configuration as top_build_configuration


class TestTopBuildConfiguration(unittest.TestCase):
    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'


    def test_typical_1(self):
        reference_expected = ['AliceAndBob.xml', 'ExampleNode.xml']
        obj = top_build_configuration.TopBuildConfiguration(self.__data_dir + os.sep + 'tbc_typical.xml')
        reference_result = obj.get_references_in_relative_path()

        self.assertEqual(self.__data_dir + os.sep + 'tbc_typical.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual(reference_expected, reference_result)


    def test_typical_2(self):
        reference_expected = []
        obj = top_build_configuration.TopBuildConfiguration(self.__data_dir + os.sep + 'tbc_empty.xml')
        reference_result = obj.get_references_in_relative_path()

        self.assertEqual(self.__data_dir + os.sep + 'tbc_empty.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual(reference_expected, reference_result)


    def test_error_specidied_path_is_not_file(self):
        with self.assertRaises(FileNotFoundError):
            top_build_configuration.TopBuildConfiguration(self.__data_dir + os.sep + 'does_not_exist.xml')
        with self.assertRaises(FileNotFoundError):
            top_build_configuration.TopBuildConfiguration('.') # specify directory


    def test_error_not_formed(self):
        with self.assertRaises(xml.etree.ElementTree.ParseError):
            top_build_configuration.TopBuildConfiguration(self.__data_dir + os.sep + 'tbc_not_formed.xml')


if __name__ == '__main__':
    # executed
    unittest.main()
