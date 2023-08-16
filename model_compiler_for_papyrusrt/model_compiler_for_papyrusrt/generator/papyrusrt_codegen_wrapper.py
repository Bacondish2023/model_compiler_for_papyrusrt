#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@file papyrusrt_codegen_wrapper.py
@brief Generates code from specified model with Papyrus-RT standalone code generator
@note This source code is derived work of umlrtgen.sh licensed under the Eclipse Public License Version 1.0.
      The umlrtgen.sh is available in the Papyrus-RT and its copyright is on Papyrus-RT developers.
'''


import os
import sys
import getopt
import re
import subprocess
import platform
import logging
import traceback


class PapyrusrtCodegenWrapper:


    def __init__(self, plugin_dir, java_command):
        '''
        @brief Constructor.
        @param[in] plugin_dir   Root of plug-in directory
        @param[in] java_command Command which launches the Java VM
        '''

        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__plugin_dir = plugin_dir
        self.__java_command = java_command

        # List of class paths. List of str type.
        self.__class_path = []

        # Standalone code generator
        self.__find_package('org.eclipse.papyrusrt.codegen.standalone')

        # Other Papyrus-RT packages
        self.__find_package('org.eclipse.papyrusrt.codegen')
        self.__find_package('org.eclipse.papyrusrt.codegen.config')
        self.__find_package('org.eclipse.papyrusrt.codegen.cpp.profile')
        self.__find_package('org.eclipse.papyrusrt.codegen.cpp')
        self.__find_package('org.eclipse.papyrusrt.codegen.cpp.rts')
        self.__find_package('org.eclipse.papyrusrt.codegen.cpp.statemachines.flat')
        self.__find_package('org.eclipse.papyrusrt.codegen.cpp.structure')
        self.__find_package('org.eclipse.papyrusrt.codegen.lang')
        self.__find_package('org.eclipse.papyrusrt.codegen.lang.cpp')
        self.__find_package('org.eclipse.papyrusrt.codegen.statemachines.flat')
        self.__find_package('org.eclipse.papyrusrt.codegen.utils')
        self.__find_package('org.eclipse.papyrusrt.codegen.papyrus')
        self.__find_package('org.eclipse.papyrusrt.umlrt.profile')
        self.__find_package('org.eclipse.papyrusrt.umlrt.uml')
        self.__find_package('org.eclipse.papyrusrt.umlrt.common.rts.library')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.aexpr')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.aexpr.uml')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.common.model')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.config')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.external')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.interactions.model')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.statemach.model')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.statemach.ext.model')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.trans')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.trans.from.uml')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.umlrt.model')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.util')
        self.__find_package('org.eclipse.papyrusrt.xtumlrt.xtext')

        # Other required packages
        self.__find_package('com.google.guava')
        self.__find_package('com.google.inject')
        self.__find_package('javax.inject')
        self.__find_package('org.apache.commons.cli')
        self.__find_package('org.eclipse.core.runtime')
        self.__find_package('org.eclipse.emf.codegen.ecore')
        self.__find_package('org.eclipse.emf.common')
        self.__find_package('org.eclipse.emf.ecore')
        self.__find_package('org.eclipse.emf.ecore.xmi')
        self.__find_package('org.eclipse.emf.mapping.ecore2xml')
        self.__find_package('org.eclipse.equinox.common')
        self.__find_package('org.eclipse.equinox.registry')
        self.__find_package('org.eclipse.ocl')
        self.__find_package('org.eclipse.osgi')
        self.__find_package('org.eclipse.papyrus.designer.languages.cpp.library')
        self.__find_package('org.eclipse.uml2.codegen.ecore')
        self.__find_package('org.eclipse.uml2.common')
        self.__find_package('org.eclipse.uml2.types')
        self.__find_package('org.eclipse.uml2.uml')
        self.__find_package('org.eclipse.uml2.uml.profile.standard')
        self.__find_package('org.eclipse.uml2.uml.resources')
        self.__find_package('org.eclipse.xtext.xbase.lib')


    def generate(self, model_path, top_capsule, out_dir, log_level, enable_stack_trace):
        '''
        @brief Generates code with Papyrus-RT
        @param[in] model_path         Path to model(.uml) file which includs the extension
        @param[in] top_capsule        Top capsule name
        @param[in] out_dir            Output directory
        @param[in] log_level          One of followings
                                      ('OFF', 'SEVERE', 'INFO', 'WARNING', 'CONFIG', 'FINE', 'FINER', 'FINEST')
        @param[in] enable_stack_trace True: enabled, False: disabled
        @exception CalledProcessError Papyrus-RT returns non-zero status
        @exception ValueError         log_level is wrong
        '''

        # check
        log_level_candidates = ('OFF', 'SEVERE', 'INFO', 'WARNING', 'CONFIG', 'FINE', 'FINER', 'FINEST')
        if log_level not in log_level_candidates:
            raise ValueError('Specified "{0}" is not log level'.format(log_level))

        # operation
        arguments = [
            self.__java_command,
            '-cp', self.__get_classpath_str(),
            'org.eclipse.papyrusrt.codegen.standalone.StandaloneUMLRTCodeGenerator',
            '--plugins', self.__plugin_dir,
            '--loglevel', log_level,
            '--outdir', out_dir,
            '--top', top_capsule,
            ]

        if enable_stack_trace:
            arguments += ['--prtrace']
        else:
            pass # nothing to do

        arguments += [model_path]

        self.__logger.info('Invoke Papyrus-RT')
        self.__logger.debug('Papyrus-RT arguments: {0}'.format(arguments))

        p = subprocess.run(arguments, check=True)
        return True


    def __append_classpath(self, path):
        '''
        @brief Add specified path to list of class paths.
        '''
        if len(path) > 0:
            self.__class_path.append(path)
        else:
            # nothing to do
            pass


    def __get_classpath_str(self):
        '''
        @brief      Returns classpath in joined string.
        @details    Return is joined with charactor based on platform(':' or ';')
        '''
        return os.pathsep.join(self.__class_path)


    def __find_package(self, name):
        '''
        @brief      Finds specified plug-in package.
        @details    If specified packagfe is found, its absolute path is stored to class path.
                    Otherwise, does nothing.

                    Typical behavior
                    - run with parameter "com.google.inject"
                    - "com.google.inject_3.0.0.v201605172100.jar"
                      or "com.google.inject_3.0.0.v201605172100/" is found
        '''
        # jar file
        for root, dirs, files in os.walk(self.__plugin_dir):
            for f in files:
                pattern = '^{0}_.*\.jar'.format(re.escape(name))
                if re.match(pattern, f):
                    self.__append_classpath(root + os.sep + f)
                    self.__logger.debug('Package "{0}" is found'.format(f))
                    return

        # directory which has .class file
        for root, dirs, files in os.walk(self.__plugin_dir):
            for d in dirs:
                if d.startswith(name + '_') and os.path.isdir(root + os.sep + d + os.sep + 'META-INF'):
                    self.__append_classpath(root + os.sep + d)
                    self.__logger.debug('Package "{0}" is found'.format(d))
                    return

        self.__logger.debug('Package specified "{0}" is not found'.format(name))


class PapyrusrtCodegenWrapperStub:


    def __init__(self, plugin_dir, java_command):
        '''
        @brief Constructor. Keep same with real implementation.
        '''
        pass # nothing to do


    def generate(self, model_path, top_capsule, out_dir, log_level, enable_stack_trace):
        '''
        @brief Generates code. Keep same with real implementation.
        @details Creates following files in out_dir/src
        - [top_capsule]Main.cc
        - [top_capsule]Controller.hh
        - [top_capsule]Controller.cc
        - [top_capsule].hh
        - [top_capsule].cc
        - Foo.hh
        - Foo.cc
        - Bar.hh
        - CMakeLists.txt
        - Makefile
        - Makefile[top_capsule].mk
        - [top_capsule]-connections.log

        Source files are build-able.
        '''
        path_destination = out_dir + os.sep + 'src'
        if not os.path.isdir(path_destination):
            os.makedirs(path_destination)

        ##########
        path = path_destination + os.sep + 'TopMain.cc'
        content = '''
#include "TopControllers.hh"
#include <stdio.h>

int main( int argc, char * argv[] )
{
    printHello();

    return 0;
}
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'TopControllers.hh'
        content = '''

'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'TopControllers.cc'
        content = '''
#include "TopControllers.hh"
#include "Top.hh"
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Top.hh'
        content = '''
#ifndef TOP_HH
#define TOP_HH

#include <stdio.h>

void printHello();

#endif
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Top.cc'
        content = '''
#include "Top.hh"

void printHello()
{
    printf("Hello, World!!!\n")
}
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Foo.hh'
        content = '''

'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Foo.cc'
        content = '''
#include "Foo.hh"
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Bar.hh'
        content = '''

'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'CMakeLists.txt'
        content = '''
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Makefile'
        content = '''
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'MakefileTop.mk'
        content = '''
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)

        ##########
        path = path_destination + os.sep + 'Top-connections.log'
        content = '''
'''[1:]
        with open(path, 'w') as fp:
            fp.write(content + os.linesep)


def main():
    plugin_dir = None
    java_command = None
    model_path = None
    top_capsule = None
    out_dir = None
    log_level = 'OFF'
    enable_stack_trace = False

    # ---> check argument
    if len(sys.argv) < 6:
        if len(sys.argv) == 2:
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
        else:
            printUsage()
            sys.exit(1)
    else:
        plugin_dir = os.path.abspath(sys.argv[len(sys.argv) - 5])
        java_command = sys.argv[len(sys.argv) - 4]
        model_path = sys.argv[len(sys.argv) - 3]
        top_capsule = sys.argv[len(sys.argv) - 2]
        out_dir = sys.argv[len(sys.argv) - 1]

        try:
            opts, args = getopt.getopt(
                sys.argv[1:],
                'l:s',
                ['loglevel=', 'prtrace']
            )
        except getopt.GetoptError as err:
            print(err)
            printUsage()
            sys.exit(1)
        for o, a in opts:
            if (o == '-l') or (o == '--loglevel'):
                log_level = a
            if (o == '-s') or (o == '--prtrace'):
                enable_stack_trace = True
    # <--- check argument

    # ---> operation
    try:
        generator = PapyrusrtCodegenWrapper(plugin_dir, java_command)
        generator.generate(model_path, top_capsule, out_dir, log_level, enable_stack_trace)
    except:
        traceback.print_exc()
        sys.exit(1)
    # <--- operation


def printUsage():
    print('Usage:')
    print('    {0} [options] plugin_dir java_command model_file top_capsule out_dir'.format(os.path.basename(__file__)))
    print('    {0} --help'.format(os.path.basename(__file__)))
    print('')
    print('Required parameters:')
    print('    plugin_dir   Root of plug-in directory.')
    print('                 Typically [Your installation directory]/Papyrus-RT/plugins,')
    print('    java_command Command which launches the Java VM.')
    print('                 Typically "java".')
    print('    model_file   Path to model(.uml) file which includs the extension')
    print('    top_capsule  Top capsule name')
    print('    out_dir      Output directory.')
    print('                 Papyrus-RT creates directory out_dir/src and deploys codes.')
    print('                 Single directory name needs leading "./". e.g. "./zzz_codegen"')
    print('')
    print('Options:')
    print('    -l, --loglevel LEVEL One of followings.')
    print('                         (OFF, SEVERE, INFO, WARNING, CONFIG, FINE, FINER, FINEST).')
    print('                         The default is OFF')
    print('    -s, --prtrace        Print the stack trace for exceptions')
    print('')
    print('Print help:')
    print('    -h, --help           Show help')


if __name__ == '__main__':
    # executed
    main()
else:
    # imported
    pass
