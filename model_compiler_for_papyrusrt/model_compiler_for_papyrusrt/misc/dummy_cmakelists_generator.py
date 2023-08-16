#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file dummy_cmakelists_generator.py
@brief Generates dummy CMakeLists.txt
@details Creates empty CMakeLists.txt whose timestamp is very old.
         Purpose: code(includes CMakeLists.txt) generation with CMake build process
         and integration of generated code as subdirectory.
         There is a constraint that
         CMake's add_subdirectory() requires sub-directory and sub-CMakeLists.txt
         at cmake run(makefile generation).
         So, with generating dummy we can integrate code generation in CMake build process.
'''


import os
import sys
import getopt
import time


class DummyCMakeListsGenerator:


    def __init__(self):
        '''
        @brief Constructor
        '''
        pass # nothing to do


    def generate(self, path_output_dir):
        '''
        @brief Generates dummy CMakeLists.txt in specified directory
        @details if path_output_dir does not exist, this operation creates
        '''
        if len(path_output_dir) == 0:
            ValueError('Specified directory "{0}" is invalid'.format(path_output_dir))

        path_cmakelists = path_output_dir + os.sep + 'CMakeLists.txt'

        # create directory if it does not exist
        if not os.path.isdir(path_output_dir):
            os.makedirs(path_output_dir)

        # create CMakeLists.txt
        with open(path_cmakelists, mode='w') as fp:
            pass

        # make dummy very old
        atime = mtime = time.mktime((1990, 1, 1, 0, 0, 0, 0, 0, -1))
        os.utime(path_cmakelists, (atime, mtime))


def main():
    path_output_dir = None

    # ---> check argument
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    except getopt.GetoptError as err:
        print(err)
        printUsage()
        sys.exit(1)

    for o, a in opts:
        if (o == '-h') or (o == '--help'):
            printUsage()
            sys.exit(0)

    if len(sys.argv) < 2:
        print('Error: The number of arguments is invalid')
        printUsage()
        sys.exit(1)
    else:
        path_output_dir = sys.argv[1]
    # <--- check argument

    # ---> operation
    generator = DummyCMakeListsGenerator()
    generator.generate(path_output_dir)
    # <--- operation


def printUsage():
    print('Usage:')
    print('    {0} out-dir'.format(os.path.basename(__file__)))
    print('    {0} -h'.format(os.path.basename(__file__)))
    print('')
    print('Required parameters:')
    print('    <out-dir> is the output directory')
    print('')
    print('Options:')
    print('    -h       show help')


if __name__ == '__main__':
    # executed
    main()
else:
    # imported
    pass
