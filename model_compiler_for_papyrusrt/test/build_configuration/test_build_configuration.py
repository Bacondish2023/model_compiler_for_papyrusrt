#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import os
import xml.etree.ElementTree

import model_compiler_for_papyrusrt.build_configuration.build_configuration as build_configuration


class TestBuildConfiguration(unittest.TestCase):
    def setUp(self):
        self.__data_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep + 'data'


    def test_typical_executable_1(self):
        obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_1.xml')

        self.assertEqual(self.__data_dir + os.sep + 'bc_typical_executable_1.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual('AliceAndBob', obj.get_target_name())
        self.assertEqual('executable', obj.get_target_type())
        self.assertEqual('TopAliceAndBob', obj.get_top_capsule_name())
        self.assertEqual('model/Sample.uml', obj.get_model_file())

        expected_sources = [
            'TopAliceAndBob',
            'Alice',
            'Bob',
            'AliceAndBobProtocol',
        ]
        self.assertEqual(expected_sources, obj.get_sources())

        expected_controller_setting = '''
TopAliceAndBob = MainThread
TopAliceAndBob.alice = AliceThread
TopAliceAndBob.bob = BobThread
'''
        self.assertEqual(expected_controller_setting, obj.get_controller_setting())

        expected_include_directories = [
            'src',
        ]
        self.assertEqual(expected_include_directories, obj.get_include_directories())

        self.assertEqual('-DNEED_NON_FLEXIBLE_ARRAY', obj.get_compile_argument())

        expected_libraries = [
            'libumlrts',
        ]
        self.assertEqual(expected_libraries, obj.get_libraries())

        expected_library_directories = [
            'src',
        ]
        self.assertEqual(expected_library_directories, obj.get_library_directories())
        self.assertEqual(None, obj.get_link_argument())

        expected_user_declaration_preface = '''
# userDeclarationPreface
# nothing to do
'''
        self.assertEqual(expected_user_declaration_preface, obj.get_user_declaration_preface())

        expected_user_declaration_before_target = '''
# userDeclarationBeforeTarget
# nothing to do
'''
        self.assertEqual(expected_user_declaration_before_target, obj.get_user_declaration_before_target())

        expected_user_declaration_after_target = '''
# userDeclarationAfterTarget
if (MSVC)
    target_link_libraries(
        AliceAndBob
        PUBLIC
            ws2_32.lib
    )
endif ()
'''
        self.assertEqual(expected_user_declaration_after_target, obj.get_user_declaration_after_target())

        expected_user_declaration_ending = '''
# userDeclarationEnding
# nothing to do
'''
        self.assertEqual(expected_user_declaration_ending, obj.get_user_declaration_ending())


    def test_typical_executable_2(self):
        obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_2.xml')

        self.assertEqual(self.__data_dir + os.sep + 'bc_typical_executable_2.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual('AliceAndBob', obj.get_target_name())
        self.assertEqual('executable', obj.get_target_type())
        self.assertEqual('TopAliceAndBob', obj.get_top_capsule_name())
        self.assertEqual('model/Sample.uml', obj.get_model_file())

        expected_sources = [
            'TopAliceAndBob',
            'Alice',
            'Bob',
            'AliceAndBobProtocol',
        ]
        self.assertEqual(expected_sources, obj.get_sources())

        self.assertEqual(None, obj.get_controller_setting())
        self.assertEqual([], obj.get_include_directories())
        self.assertEqual(None, obj.get_compile_argument())
        self.assertEqual([], obj.get_libraries())
        self.assertEqual([], obj.get_library_directories())
        self.assertEqual(None, obj.get_link_argument())
        self.assertEqual(None, obj.get_user_declaration_preface())
        self.assertEqual(None, obj.get_user_declaration_before_target())
        self.assertEqual(None, obj.get_user_declaration_after_target())
        self.assertEqual(None, obj.get_user_declaration_ending())


    def test_typical_executable_3(self):
        obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_executable_3.xml')

        self.assertEqual(self.__data_dir + os.sep + 'bc_typical_executable_3.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual('AliceAndBob', obj.get_target_name())
        self.assertEqual('executable', obj.get_target_type())
        self.assertEqual('TopAliceAndBob', obj.get_top_capsule_name())
        self.assertEqual('model/Sample.uml', obj.get_model_file())

        expected_sources = [
            'TopAliceAndBob',
        ]
        self.assertEqual(expected_sources, obj.get_sources())

        expected_include_directories = [
            'src',
        ]
        self.assertEqual(expected_include_directories, obj.get_include_directories())

        self.assertEqual(None, obj.get_compile_argument())

        expected_libraries = [
            'libumlrts',
        ]
        self.assertEqual(expected_libraries, obj.get_libraries())

        expected_library_directories = [
            'src',
        ]
        self.assertEqual(expected_library_directories, obj.get_library_directories())
        self.assertEqual(None, obj.get_link_argument())
        self.assertEqual(None, obj.get_user_declaration_preface())
        self.assertEqual(None, obj.get_user_declaration_before_target())
        self.assertEqual(None, obj.get_user_declaration_after_target())
        self.assertEqual(None, obj.get_user_declaration_ending())


    def test_typical_library(self):
        obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_typical_library.xml')

        self.assertEqual(self.__data_dir + os.sep + 'bc_typical_library.xml', obj.get_path_to_configuration_file())
        self.assertEqual('1.0', obj.get_version_string())
        self.assertEqual('libfoo', obj.get_target_name())
        self.assertEqual('library', obj.get_target_type())
        self.assertEqual('Top', obj.get_top_capsule_name())
        self.assertEqual('model/Sample.uml', obj.get_model_file())

        expected_sources = [
            'Top',
        ]
        self.assertEqual(expected_sources, obj.get_sources())
        self.assertEqual([], obj.get_include_directories())
        self.assertEqual(None, obj.get_compile_argument())
        self.assertEqual([], obj.get_libraries())
        self.assertEqual([], obj.get_library_directories())
        self.assertEqual(None, obj.get_link_argument())
        self.assertEqual(None, obj.get_user_declaration_preface())
        self.assertEqual(None, obj.get_user_declaration_before_target())
        self.assertEqual(None, obj.get_user_declaration_after_target())
        self.assertEqual(None, obj.get_user_declaration_ending())


    def test_error_specidied_path_is_not_file(self):
        with self.assertRaises(FileNotFoundError):
            build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'does_not_exist.xml')
        with self.assertRaises(FileNotFoundError):
            build_configuration.BuildConfiguration('.') # specify directory


    def test_error_00_version_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_00_version_missing.xml')


    def test_error_10_target_name_element_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_10_target_name_element_missing.xml')


    def test_error_11_target_name_content_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_11_target_name_content_missing.xml')


    def test_error_12_target_name_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_12_target_name_invalid.xml')


    def test_error_20_target_type_element_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_20_target_type_element_missing.xml')


    def test_error_21_target_type_invalid(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_21_target_type_invalid.xml')


    def test_error_30_top_capsule_name_element_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_30_top_capsule_name_element_missing.xml')


    def test_error_40_model_file_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_40_model_file_missing.xml')


    def test_error_50_source_element_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_50_source_element_missing.xml')


    def test_error_51_source_content_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_51_source_content_missing.xml')


    def test_error_52_source_invalid(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_52_source_invalid.xml')


    def test_error_60_controller_setting_element_missing(self):
        with self.assertRaises(ValueError):
            obj = build_configuration.BuildConfiguration(self.__data_dir + os.sep + 'bc_error_60_controller_setting_element_missing.xml')


if __name__ == '__main__':
    # executed
    unittest.main()
