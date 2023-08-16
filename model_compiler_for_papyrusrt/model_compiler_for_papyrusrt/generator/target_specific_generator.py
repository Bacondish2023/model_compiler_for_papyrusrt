#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import glob
import shutil
import logging

import model_compiler_for_papyrusrt.build_configuration.build_configuration as build_configuration
import model_compiler_for_papyrusrt.generator.papyrusrt_codegen_wrapper as papyrusrt_codegen_wrapper
import model_compiler_for_papyrusrt.generator.target_specific_cmakelists_generator as target_specific_cmakelists_generator

class TargetSpecificGenerator:


    def __init__(self, configuration, project_root_dir, codegen_dir, papyrusrt_root_dir, use_stub = False):
        '''
        @brief Constructor
        @param[in] configuration instance of BuildConfiguration
        @param[in] project_root_dir path to project root directory
        @param[in] codegen_dir path to codegen directory
        @param[in] papyrusrt_root_dir path to papyrusrt root directory
        @param[in] use_stub True: useing PapyrusrtCodegenWrapperStub, False: using PapyrusrtCodegenWrapper
        '''
        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__configuration = configuration
        self.__project_root_dir = project_root_dir
        self.__codegen_dir = codegen_dir
        self.__papyrusrt_root_dir = papyrusrt_root_dir
        self.__use_stub = use_stub


    def generateIfRequired(self):
        path_to_cmakelists = self.__codegen_dir + os.sep + self.__configuration.get_target_name() + os.sep + 'CMakeLists.txt'
        path_to_configuration_file = self.__configuration.get_path_to_configuration_file()
        path_to_model = self.__project_root_dir + os.sep + self.__configuration.get_model_file()

        isRequired = False
        if os.path.isfile(path_to_cmakelists):
            if (    (os.path.getmtime(path_to_cmakelists) < os.path.getmtime(path_to_configuration_file))
                 or (os.path.getmtime(path_to_cmakelists) < os.path.getmtime(path_to_model))):
                isRequired = True
            else:
                isRequired = False
        else:
            isRequired = True

        if isRequired:
            self.__logger.info('Model-compile {0}'.format(self.__configuration.get_target_name()))
            self._generate()
        else:
            # nothing to do
            self.__logger.info('Skip to model-compile {0}'.format(self.__configuration.get_target_name()))


    def _generate(self):
        # create controllers file
        path_model_directory = os.path.dirname(self.__project_root_dir + os.sep + self.__configuration.get_model_file())
        filename = self.__configuration.get_top_capsule_name() + '.controllers'
        path_controllers_file =  path_model_directory + os.sep + filename

        self.__logger.debug('Try to create controllers file "{0}"'.format(path_controllers_file))
        if os.path.exists(path_controllers_file):
            self.__logger.warning('File or directory "{0}" already exists. Overwrite.'.format(path_controllers_file))
        else:
            pass # nothing to do

        with open(path_controllers_file, 'w') as fp:
            content = self.__configuration.get_controller_setting()
            if content is None:
                content = ''
            fp.write(content)
        self.__logger.info('Create controllers file "{0}".'.format(path_controllers_file))

        # generate
        self._codegen_with_papyrusrt()
        self._arrange_codegen_dir()

        # save controllers file
        path_controllers_file_saved = self.__codegen_dir + os.sep + self.__configuration.get_target_name() + os.sep + filename
        shutil.move(path_controllers_file, path_controllers_file_saved)
        self.__logger.info('Save controllers file into "{0}".'.format(path_controllers_file_saved))


    def _codegen_with_papyrusrt(self):
        # construct codegen
        plugin_dir = self.__papyrusrt_root_dir + os.sep + 'plugins'
        java_vm = 'java'

        codegen = None
        if self.__use_stub:
            self.__logger.debug('Using PapyrusrtCodegenWrapperStub')
            codegen = papyrusrt_codegen_wrapper.PapyrusrtCodegenWrapperStub(plugin_dir, java_vm)
        else:
            self.__logger.debug('Using PapyrusrtCodegenWrapper')
            codegen = papyrusrt_codegen_wrapper.PapyrusrtCodegenWrapper(plugin_dir, java_vm)

        # run
        model_path = self.__project_root_dir + os.sep + self.__configuration.get_model_file()
        top_capsule = self.__configuration.get_top_capsule_name()
        out_dir = self.__codegen_dir + os.sep + self.__configuration.get_target_name()
        log_level = 'WARNING'
        enable_stack_trace = False

        codegen.generate(
            model_path,
            top_capsule,
            out_dir,
            log_level,
            enable_stack_trace,
        )


    def _arrange_codegen_dir(self):
        top_capsule_name = self.__configuration.get_top_capsule_name()
        out_dir = self.__codegen_dir + os.sep + self.__configuration.get_target_name()
        src_dir = out_dir + os.sep + 'src'

        # remove unnecessary build scripts
        target_path = src_dir + os.sep + 'CMakeLists.txt'
        if os.path.isfile(target_path):
            os.remove(target_path)

        target_path = src_dir + os.sep + 'Makefile'
        if os.path.isfile(target_path):
            os.remove(target_path)

        target_path = src_dir + os.sep + 'Makefile' + top_capsule_name + '.mk'
        if os.path.isfile(target_path):
            os.remove(target_path)

        # remove unnecessary source files
        out_dir = self.__codegen_dir + os.sep + self.__configuration.get_target_name()
        for file in glob.glob(out_dir + os.sep + 'src' + os.sep + '*'):
            if self.__is_source_file(file):
                if self.__is_necessary_source_file(file):
                    pass # nothing to do
                else:
                    self.__logger.debug('Remove unnecessary file {0}'.format(os.path.abspath(file)))
                    os.remove(file)

        # logging about generated file
        for source in self.__configuration.get_sources():
            if (    os.path.isfile(out_dir + os.sep + 'src' + os.sep + source + '.hh')
                or  os.path.isfile(out_dir + os.sep + 'src' + os.sep + source + '.cc')):
                self.__logger.info('Generated {0}'.format(source))
            else:
                if (self.__configuration.get_target_type() == 'library') and (source == top_capsule_name):
                    pass # nothing to do. top capsule is not generated for library build type.
                else:
                    self.__logger.warning('There is no generated file for {0}. Make sure {0} is in the model'.format(source))

        # create implementation file list for build
        implementation_files = []

        if self.__configuration.get_target_type() == 'executable':
            implementation_files.append('src/' + top_capsule_name + 'Main.cc')
            implementation_files.append('src/' + top_capsule_name + 'Controllers.cc')
            implementation_files.append('src/' + top_capsule_name + '.cc')
        else:
            pass

        for file in glob.glob(out_dir + os.sep + 'src' + os.sep + '*.cc'):
            if self.__is_necessary_source_file(file):
                implementation_filename = 'src/' + os.path.basename(file)
                if implementation_filename in implementation_files:
                    pass # nothing to do. should be top*.cc
                else:
                    implementation_files.append(implementation_filename)


        # generate CMakeLists.txt
        cmakelists_gen = target_specific_cmakelists_generator.TargetSpecificCMakeListsGenerator(
            out_dir,
            self.__configuration,
            implementation_files,
        )
        cmakelists_gen.generate()


    def __is_header_file(self, path):
        filename = os.path.basename(path)
        extension = os.path.splitext(filename)[1]

        if extension == '.hh':
            return True
        else:
            return False


    def __is_implementation_file(self, path):
        filename = os.path.basename(path)
        extension = os.path.splitext(filename)[1]

        if extension == '.cc':
            return True
        else:
            return False


    def __is_source_file(self, path):
        if self.__is_header_file(path) or self.__is_implementation_file(path):
            return True
        else:
            return False


    def __is_necessary_source_file(self, path):
        filename = os.path.basename(path)
        top_capsule_name = self.__configuration.get_top_capsule_name()

        necessary_filename_candidates = []

        if self.__configuration.get_target_type() == 'executable':
            necessary_filename_candidates.append(top_capsule_name + 'Main.cc')
            necessary_filename_candidates.append(top_capsule_name + 'Controllers.hh')
            necessary_filename_candidates.append(top_capsule_name + 'Controllers.cc')
        else:
            pass

        for source_element_name in self.__configuration.get_sources():
            if (self.__configuration.get_target_type() == 'library') and (source_element_name == top_capsule_name):
                pass
            else:
                filename_header = source_element_name + '.hh'
                filename_implementation = source_element_name + '.cc'
                if filename_header not in necessary_filename_candidates:
                    necessary_filename_candidates.append(filename_header)
                if filename_implementation not in necessary_filename_candidates:
                    necessary_filename_candidates.append(filename_implementation)


        if self.__is_source_file(filename):
            if filename in necessary_filename_candidates:
                return True
            else:
                return False
        else:
            return False


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
