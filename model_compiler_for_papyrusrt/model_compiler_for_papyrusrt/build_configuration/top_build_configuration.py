#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import xml.etree.ElementTree


class TopBuildConfiguration:


    def __init__(self, path):
        '''
        @brief Constructor
        @param[in] path path to BuildConfiguration file
        @exception FileNotFoundError Specified path is not file
        @exception xml.etree.ElementTree.ParseError Specified file is not well-formed XML
        '''

        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__root = None
        self.__abs_path = None

        self.__version_string = None
        self.__references = []

        # check
        if not os.path.isfile(path):
            raise FileNotFoundError('Specified path "{0}" is not file'.format(path))

        # init attributes
        self.__abs_path = os.path.abspath(path)

        # parse
        self.__logger.debug('Parse TopBuildConfiguration {0}'.format(self.__abs_path))
        tree = xml.etree.ElementTree.parse(path)
        self.__root = tree.getroot()

        self.__parse_version_string()
        self.__parse_references()


    def get_path_to_configuration_file(self):
        '''
        @brief Returns absolute path to TopBuildConfiguration file
        '''
        return self.__abs_path


    def get_version_string(self):
        '''
        @brief Returns version string
        @return str type
        '''
        return self.__version_string


    def get_references_in_relative_path(self):
        '''
        @brief Returns list of paths wich index to BuildConfiguration file
        @return list of paths. list of str type.
        '''
        return self.__references


    def get_references_in_absolute_path(self):
        '''
        @brief Returns list of paths wich index to BuildConfiguration file
        @return list of paths. list of str type.
        '''
        references = []
        for reference in self.__references:
            references.append(self.__abs_dir_path + os.sep + reference)
        return references


    def __parse_version_string(self):
        value = self.__root.attrib['version']
        if value is None:
            raise ValueError('Version is not in TopBuildConfiguration file')
        else:
            self.__version_string = value.strip()


    def __parse_references(self):
        xpath = 'reference'
        for item in self.__root.findall(xpath):
            key = 'relativePath'
            if key in item.attrib:
                if len(item.attrib[key].strip()) == 0:
                    self.__logger.debug('Attribute "{0}": "{1}" is invalid. Ignored.'.format(key, item.attrib[key]))
                else:
                    self.__references.append(item.attrib[key].strip())
            else:
                self.__logger.debug('Element "{0}" does not have attribute "{1}". Ignored.'.format(item, key))


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
