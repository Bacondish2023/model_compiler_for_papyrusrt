#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import getopt
import traceback
import logging


import model_compiler_for_papyrusrt.application as application


def main():
    project_root_dir  = None
    codegen_dir = None
    path_to_top_build_configuration = None
    loglevel = 'WARNING'
    # ---> check argument
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hl:', ['help', 'loglevel='])
    except getopt.GetoptError as err:
        print(err)
        printUsage()
        sys.exit(1)

    for o, a in opts:
        if (o == '-h') or (o == '--help'):
            printUsage()
            sys.exit(0)
        if (o == '-l') or (o == '--loglevel'):
            loglevel_candidates = {'OFF', 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'}
            if a in loglevel_candidates:
                loglevel = a
            else:
                printUsage()
                sys.exit(1)

    if len(sys.argv) < 4:
        printUsage()
        sys.exit(1)

    project_root_dir = sys.argv[len(sys.argv) - 3]
    codegen_dir = sys.argv[len(sys.argv) - 2]
    path_to_top_build_configuration = sys.argv[len(sys.argv) - 1]
    # <--- check argument

    # ---> setting
    if loglevel == 'OFF':
        logging.basicConfig(level='WARNING')
        logging.disable(logging.CRITICAL)
    else:
        root_handler = logging.StreamHandler()
        root_handler.setLevel(loglevel)

        logging.basicConfig(
            format = '%(asctime)s %(levelname)s: %(message)s',
            level = loglevel,
            handlers = [root_handler]
        )
    # <--- setting

    # ---> operation
    try:
        app = application.Application(project_root_dir, codegen_dir, path_to_top_build_configuration)
        app.main()
    except:
        traceback.print_exc()
        sys.exit(1)
    # <--- operation


def printUsage():
    print('Usage:')
    print('    {0} [options] project_root codegen_dir top_build_configuration'.format('model_compiler_for_papyrusrt'))
    print('    {0} -h'.format('model_compiler_for_papyrusrt'))
    print('')
    print('Required parameters:')
    print('    project_root             the project root directory.')
    print('                             if this does not exist, exception will be raised')
    print('    codegen_dir              the codegen directory.')
    print('                             if this does not exist, directory will be created on specified path')
    print('    top_build_configuration  the project root directory.')
    print('                             if this does not exist, exception will be raised')
    print('')
    print('Options:')
    print('    -l, --loglevel LEVEL     log-level: Set the level of logging')
    print('                             one of {OFF, CRITICAL, ERROR, WARNING, INFO, DEBUG}.')
    print('                             The default is WARNING.')
    print('')
    print('Print help:')
    print('  -h, --help: show help message')
    print('')
    print('Required environment variable:')
    print('    PAPYRUSRT_ROOT           Papyrus-RT root directory.')


if __name__ == '__main__':
    # executed
    main()
