#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import xml.etree.ElementTree


class BuildConfiguration:


    def __init__(self, path):
        '''
        @brief Constructor
        @param[in] path path to BuildConfiguration file
        @exception FileNotFoundError Specified path is not file
        @exception xml.etree.ElementTree.ParseError Specified file is not well-formed XML
        @exception ValueError When specified BuildConfiguration is invalid
        '''

        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__root = None
        self.__abs_path = None

        self.__version_string = None
        self.__target_name = None
        self.__target_type = None
        self.__top_capsule_name = None
        self.__model_file = None
        self.__sources = []
        self.__controller_setting = None
        self.__include_directories = []
        self.__compile_argument = None
        self.__libraries = []
        self.__library_directories = []
        self.__link_argument = None
        self.__user_declaration_preface = None
        self.__user_declaration_before_target = None
        self.__user_declaration_after_target = None
        self.__user_declaration_ending = None

        # check
        if not os.path.isfile(path):
            raise FileNotFoundError('Specified path "{0}" is not file'.format(path))

        # init attributes
        self.__abs_path = os.path.abspath(path)

        # parse
        self.__logger.debug('Parse BuildConfiguration {0}'.format(self.__abs_path))
        tree = xml.etree.ElementTree.parse(path)
        self.__root = tree.getroot()

        self.__parse_version_string()
        self.__parse_target_name()
        self.__parse_target_type()
        self.__parse_top_capsule_name()
        self.__parse_model_file()
        self.__parse_sources()
        self.__parse_controller_setting()
        self.__parse_include_directories()
        self.__parse_compile_argument()
        self.__parse_libraries()
        self.__parse_library_directories()
        self.__parse_link_argument()
        self.__parse_user_declaration_preface()
        self.__parse_user_declaration_before_target()
        self.__parse_user_declaration_after_target()
        self.__parse_user_declaration_ending()


    def get_path_to_configuration_file(self):
        '''
        @brief Returns absolute path to BuildConfiguration file
        '''
        return self.__abs_path


    def get_version_string(self):
        '''
        @brief Returns version string
        @return str type
        '''
        return self.__version_string


    def get_target_name(self):
        '''
        @brief Returns target name
        @return str type
        '''
        return self.__target_name


    def get_target_type(self):
        '''
        @brief Returns target type
        @return str type
        '''
        return self.__target_type


    def get_top_capsule_name(self):
        '''
        @brief Returns top capsule name
        @return str type
        '''
        return self.__top_capsule_name


    def get_model_file(self):
        '''
        @brief Returns path to model file from project top directory.
        @return str type
        '''
        return self.__model_file


    def get_sources(self):
        '''
        @brief Returns list of sources
        @return list of sources. list of str type.
        '''
        return self.__sources


    def get_controller_setting(self):
        '''
        @brief Returns controller setting
        @return str type
        '''
        return self.__controller_setting


    def get_include_directories(self):
        '''
        @brief Returns list of include directories
        @return list of sources. list of str type.
        '''
        return self.__include_directories


    def get_compile_argument(self):
        '''
        @brief Returns compile argument or None
        '''
        return self.__compile_argument


    def get_libraries(self):
        '''
        @brief Returns list of libraries
        @return list of libraries. list of str type.
        '''
        return self.__libraries


    def get_library_directories(self):
        '''
        @brief Returns list of library directories
        @return list of library directories. list of str type.
        '''
        return self.__library_directories


    def get_link_argument(self):
        '''
        @brief Returns link argument
        @return str type
        '''
        return self.__link_argument


    def get_user_declaration_preface(self):
        '''
        @brief Returns user declaration preface
        @return str type
        '''
        return self.__user_declaration_preface


    def get_user_declaration_before_target(self):
        '''
        @brief Returns user declaration before target
        @return str type
        '''
        return self.__user_declaration_before_target


    def get_user_declaration_after_target(self):
        '''
        @brief Returns user declaration after target
        @return str type
        '''
        return self.__user_declaration_after_target


    def get_user_declaration_ending(self):
        '''
        @brief Returns user declaration ending
        @return str type
        '''
        return self.__user_declaration_ending


    def __parse_version_string(self):
        value_raw = None
        value_stripped = None

        if 'version' in self.__root.attrib:
            value_raw = self.__root.attrib['version']
        else:
            raise ValueError('{0} is not in BuildConfiguration file'.format('version attribute'))

        value_stripped = value_raw.strip()
        if value_stripped != value_raw:
            self.__logger.warning('"{0}" value "{1}" includes space. Stripped.'.format('version attribute', value_raw))

        if len(value_stripped) == 0:
            raise ValueError('"{0}" value "{1}" is invalid'.format('version attribute', value_raw))
        else:
            self.__version_string = value_stripped


    def __parse_target_name(self):
        xpath = 'targetName'
        self.__target_name = self.__parse_mandatory_item_stripped(xpath)


    def __parse_target_type(self):
        xpath = 'targetType'
        value = self.__parse_mandatory_item_stripped(xpath)
        if value not in ('executable', 'library'):
            raise ValueError('{0} value "{1}" is invalid'.format(xpath, str(value)))
        else:
            self.__target_type = value


    def __parse_top_capsule_name(self):
        xpath = 'topCapsuleName'
        self.__top_capsule_name = self.__parse_mandatory_item_stripped(xpath)


    def __parse_model_file(self):
        xpath = 'modelFile'
        self.__model_file = self.__parse_mandatory_item_stripped(xpath)


    def __parse_sources(self):
        xpath = 'sources/source'
        for item in self.__root.findall(xpath):
            if item.text is None:
                self.__logger.debug('"{0}" does not have content. Ignored.'.format(xpath))
            else:
                value_raw = item.text
                value_stripped = value_raw.strip()

                if value_stripped != value_raw:
                    self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

                if len(value_stripped) == 0:
                    self.__logger.debug('"{0}" value "{1}" is invalid. Ignored.'.format(xpath, value_stripped))
                else:
                    self.__sources.append(value_stripped)

        if len(self.__sources) == 0:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))


    def __parse_controller_setting(self):
        xpath = 'controllerSetting'
        self.__controller_setting = self.__parse_optional_item(xpath)


    def __parse_include_directories(self):
        xpath = 'includeDirectories/includeDirectory'
        for item in self.__root.findall(xpath):
            if item.text is None:
                self.__logger.debug('"{0}" does not have content. Ignored.'.format(xpath))
            else:
                value_raw = item.text
                value_stripped = value_raw.strip()

                if value_stripped != value_raw:
                    self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

                if len(value_stripped) == 0:
                    self.__logger.debug('"{0}" value "{1}" is invalid. Ignored.'.format(xpath, value_stripped))
                else:
                    self.__include_directories.append(value_stripped)


    def __parse_compile_argument(self):
        xpath = 'compileArgument'
        self.__compile_argument = self.__parse_optional_item_stripped(xpath)


    def __parse_libraries(self):
        xpath = 'libraries/library'
        for item in self.__root.findall(xpath):
            if item.text is None:
                self.__logger.debug('"{0}" does not have content. Ignored.'.format(xpath))
            else:
                value_raw = item.text
                value_stripped = value_raw.strip()

                if value_stripped != value_raw:
                    self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

                if len(value_stripped) == 0:
                    self.__logger.debug('"{0}" value "{1}" is invalid. Ignored.'.format(xpath, value_stripped))
                else:
                    self.__libraries.append(value_stripped)


    def __parse_library_directories(self):
        xpath = 'libraryDirectories/libraryDirectory'
        for item in self.__root.findall(xpath):
            if item.text is None:
                self.__logger.debug('"{0}" does not have content. Ignored.'.format(xpath))
            else:
                value_raw = item.text
                value_stripped = value_raw.strip()

                if value_stripped != value_raw:
                    self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

                if len(value_stripped) == 0:
                    self.__logger.debug('"{0}" value "{1}" is invalid. Ignored.'.format(xpath, value_stripped))
                else:
                    self.__library_directories.append(value_stripped)


    def __parse_link_argument(self):
        xpath = 'linkArgument'
        self.__link_argument = self.__parse_optional_item_stripped(xpath)


    def __parse_user_declaration_preface(self):
        xpath = 'userDeclarationPreface'
        self.__user_declaration_preface = self.__parse_optional_item(xpath)


    def __parse_user_declaration_before_target(self):
        xpath = 'userDeclarationBeforeTarget'
        self.__user_declaration_before_target = self.__parse_optional_item(xpath)


    def __parse_user_declaration_after_target(self):
        xpath = 'userDeclarationAfterTarget'
        self.__user_declaration_after_target = self.__parse_optional_item(xpath)


    def __parse_user_declaration_ending(self):
        xpath = 'userDeclarationEnding'
        self.__user_declaration_ending = self.__parse_optional_item(xpath)


    def __parse_mandatory_item_stripped(self, xpath):
        '''
        @brief Parses content specified with xpath and return content
        @return Content(str type). Stripped(not null string).
        @exception ValueError Content specified with xpath is not found
        @exception ValueError Content specified with xpath is null or only-space string
        '''
        item = self.__root.find(xpath)
        if item is None:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))
        else:
            pass # nothing to do

        value_raw = item.text
        value_stripped = None

        if value_raw is None:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))
        else:
            pass # nothing to do

        value_stripped = value_raw.strip()
        if value_stripped != value_raw:
            self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

        if len(value_stripped) == 0:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))
        else:
            return value_stripped


    def __parse_optional_item(self, xpath):
        '''
        @brief Parses content specified with xpath and return content
        @return Content(str type) or None
        @exception ValueError Content specified with xpath is not found
        '''
        item = self.__root.find(xpath)
        if item is None:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))
        else:
            return item.text



    def __parse_optional_item_stripped(self, xpath):
        '''
        @brief Parses content specified with xpath and return content
        @return Content(str type)-stripped(not null string) or None
        @exception ValueError Content specified with xpath is not found
        '''
        item = self.__root.find(xpath)
        if item is None:
            raise ValueError('{0} is not in Target-Specific BuildConfiguration file'.format(xpath))
        else:
            pass # nothing to do

        value_raw = item.text
        value_stripped = None

        if value_raw is None:
            self.__logger.debug('"{0}" does not have content. Ignored.'.format(xpath))
            return None
        else:
            pass # nothing to do

        value_stripped = value_raw.strip()
        if value_stripped != value_raw:
            self.__logger.debug('"{0}" value "{1}" includes space. Stripped.'.format(xpath, value_raw))

        if len(value_stripped) == 0:
            self.__logger.debug('"{0}" value "{1}" is invalid. Ignored.'.format(xpath, value_stripped))
            return None
        else:
            return value_stripped


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
