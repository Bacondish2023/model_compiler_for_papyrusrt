#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree


class TargetSpecificCMakeListsGenerator:


    def __init__(self, destination_dir, configuration, source_files):
        '''
        @brief Constructor
        @param[in] destination_dir path to directory which to CMakeLists will be created
        @param[in] target_names list of targets. list of str type.
        @param[in] source_files list of source files. list of str type.
        '''
        self.__destination_dir = destination_dir
        self.__configuration = configuration
        self.__source_files = source_files


    def generate(self):
        content = self._get_str()
        path = self.__destination_dir + os.sep + 'CMakeLists.txt'

        with open(path, 'w') as fp:
            fp.write(content + os.linesep)


    def _get_str(self):
        template = '''
# @brief Build script for Papyrus-RT project
#
# Do NOT edit!!!
# Generated by the Model Compiler for Papyrus-RT

{user_declaration_preface}
{user_declaration_before_target}
{add_target_section}
{user_declaration_after_target}
{target_include_directories_section}
{target_compile_options_section}
{target_link_libraries_section}
{target_link_options_section}
{target_link_directories_section}
{user_declaration_ending}
'''[1:]

        return_str = template.format(
            user_declaration_preface = self.__get_user_declaration_preface(),
            user_declaration_before_target = self.__get_user_declaration_before_target(),
            add_target_section = self.__get_add_target_section(),
            user_declaration_after_target = self.__get_user_declaration_after_target(),
            target_include_directories_section = self.__get_target_include_directories_section(),
            target_compile_options_section = self.__get_target_compile_options_section(),
            target_link_libraries_section = self.__get_target_link_libraries_section(),
            target_link_options_section = self.__get_target_link_options_section(),
            target_link_directories_section = self.__get_target_link_options_section(),
            user_declaration_ending = self.__get_user_declaration_ending(),
        )

        return return_str


    def __get_user_declaration_preface(self):
        value = self.__configuration.get_user_declaration_preface()
        if value is None:
            return ''
        else:
            template = '''
# ---> User declaration preface
{0}
# <--- User declaration preface
'''[1:]
            return template.format(value)


    def __get_user_declaration_before_target(self):
        value = self.__configuration.get_user_declaration_before_target()
        if value is None:
            return ''
        else:
            template = '''
# ---> User declaration before target
{0}
# <--- User declaration before target
'''[1:]
            return template.format(value)


    def __get_add_target_section(self):
        template = None
        if self.__configuration.get_target_type() == 'executable':
            template = '''
add_executable( {target_name}
    {source_files}
)
'''[1:]
        else:
            template = '''
add_library( {target_name} STATIC
    {source_files}
)
'''[1:]

        return_str = template.format(
            target_name = self.__configuration.get_target_name(),
            source_files = ('\n' + '    ').join(self.__source_files),
        )

        return return_str


    def __get_user_declaration_after_target(self):
        value = self.__configuration.get_user_declaration_after_target()
        if value is None:
            return ''
        else:
            template = '''
# ---> User declaration after target
{0}
# <--- User declaration after target
'''[1:]
            return template.format(value)


    def __get_target_include_directories_section(self):
        template = '''
target_include_directories( {target_name}
    PUBLIC
        {include_directories}
)
'''[1:]

        return_str = None
        if len(self.__configuration.get_include_directories()) == 0:
            return_str = ''
        else:
            return_str = template.format(
                target_name = self.__configuration.get_target_name(),
                include_directories = ('\n' + 2 * '    ').join(self.__configuration.get_include_directories()),
            )

        return return_str


    def __get_target_compile_options_section(self):
        template = '''
target_compile_options( {target_name}
    PRIVATE
        {options}
)
'''[1:]

        return_str = None
        if self.__configuration.get_compile_argument() is None:
            return_str = ''
        else:
            return_str = template.format(
                target_name = self.__configuration.get_target_name(),
                options = self.__configuration.get_compile_argument(),
            )

        return return_str


    def __get_target_link_libraries_section(self):
        template = '''
target_link_libraries( {target_name}
    PRIVATE
        {libraries}
)
'''[1:]

        return_str = None
        if len(self.__configuration.get_libraries()) == 0:
            return_str = ''
        else:
            return_str = template.format(
                target_name = self.__configuration.get_target_name(),
                libraries = ('\n' + 2 * '    ').join(self.__configuration.get_libraries()),
            )

        return return_str


    def __get_target_link_options_section(self):
        template = '''
target_link_options( {target_name}
    PRIVATE
        {options}
)
'''[1:]

        return_str = None
        if self.__configuration.get_link_argument() is None:
            return_str = ''
        else:
            return_str = template.format(
                target_name = self.__configuration.get_target_name(),
                options = self.__configuration.get_link_argument(),
            )

        return return_str


    def __get_target_link_directories_section(self):
        template = '''
target_include_directories( {target_name}
    PUBLIC
        {library_directories}
)
'''[1:]

        return_str = None
        if len(self.__configuration.get_library_directories()) == 0:
            return_str = ''
        else:
            return_str = template.format(
                target_name = self.__configuration.get_target_name(),
                library_directories = ('\n' + 2 * '    ').join(self.__configuration.get_library_directories()),
            )

        return return_str


    def __get_user_declaration_ending(self):
        value = self.__configuration.get_user_declaration_ending()
        if value is None:
            return ''
        else:
            template = '''
# ---> User declaration ending
{0}
# <--- User declaration ending
'''[1:]
            return template.format(value)


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass