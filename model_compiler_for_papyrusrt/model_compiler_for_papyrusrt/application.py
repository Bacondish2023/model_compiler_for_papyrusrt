#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import time
import logging

import model_compiler_for_papyrusrt.build_configuration.top_build_configuration as top_build_configuration
import model_compiler_for_papyrusrt.build_configuration.build_configuration as build_configuration
import model_compiler_for_papyrusrt.generator.top_generator as top_generator
import model_compiler_for_papyrusrt.generator.target_specific_generator as target_specific_generator


class Application:
    def __init__(self, project_root_dir, codegen_dir, path_to_tbc):
        '''
        @brief Constructor
        @param[in] project_root_dir path to project root directory
        @param[in] codegen_dir path to codegen directory
        @param[in] path_top_tbc path to TopBuildConfiguration
        @exception FileNotFoundError project_root_dir is not directory
        @exception FileNotFoundError codegen_dir is not directory
        @exception FileNotFoundError path_to_tbc is not file
        @exception KeyError PAPYRUSRT_ROOT is not defined
        @exception FileNotFoundError env['PAPYRUSRT_ROOT'] is not directory
        '''

        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        # sanity check for arguments
        if not os.path.isdir(project_root_dir):
            raise FileNotFoundError('Specified path "{0}" is not directory'.format(project_root_dir))
        self.__project_root_dir = os.path.abspath(project_root_dir)

        if not os.path.isdir(codegen_dir):
            raise FileNotFoundError('Specified path "{0}" is not directory'.format(codegen_dir))
        self.__codegen_dir = os.path.abspath(codegen_dir)

        if not os.path.isfile(path_to_tbc):
            raise FileNotFoundError('Specified path "{0}" is not file'.format(path_to_tbc))
        self.__path_to_tbc = os.path.abspath(path_to_tbc)

        # sanity check for environment variable
        key = 'PAPYRUSRT_ROOT'
        self.__papyrusrt_root_dir = os.environ['PAPYRUSRT_ROOT']
        if not os.path.isdir(self.__papyrusrt_root_dir):
            raise FileNotFoundError('env[{0}] "{1}" is not directory'.format(key, self.__papyrusrt_root_dir))

        # logging
        self.__logger.info('Model Compiler for Papyrus-RT: Start')

        self.__logger.info('Project Root: {0}'.format(self.__project_root_dir))
        self.__logger.info('Codegen Directory: {0}'.format(self.__codegen_dir))
        self.__logger.info('env[PAPYRUSRT_ROOT]: {0}'.format(self.__papyrusrt_root_dir))


    def __del__(self):
        self.__logger.info('Model Compiler for Papyrus-RT: End')


    def main(self):
        # load TopBuildConfiguration file
        tbc = self.__load_tbc()

        # load BuildConfiguration files
        list_bc = self.__load_bcs(tbc)

        # create top generator
        top_generator = self.__create_top_generator(self.__project_root_dir, self.__codegen_dir, tbc, list_bc)

        # create specific generators
        list_target_names, dict_specific_generator = self.__create_specific_generators(self.__project_root_dir, self.__codegen_dir, self.__papyrusrt_root_dir, list_bc)

        # operation
        top_generator.generateIfRequired()
        for target_name in list_target_names:
            target_specific_generator = dict_specific_generator[target_name]

            start_time = time.perf_counter()
            target_specific_generator.generateIfRequired()
            end_time = time.perf_counter()
            self.__logger.info('Model-compile for {0} takes {1} msec'.format( target_name,  int((end_time - start_time) * 1000) ))


    def __load_tbc(self):
        tbc = top_build_configuration.TopBuildConfiguration(self.__path_to_tbc)
        self.__logger.info('TopBuildConfiguration {0} loaded'.format(os.path.basename(tbc.get_path_to_configuration_file())))
        return tbc


    def __load_bcs(self, top_build_configuration):
        build_configurations = []
        build_configuration_dir = os.path.dirname(top_build_configuration.get_path_to_configuration_file())

        for rpath in top_build_configuration.get_references_in_relative_path():
            bc = build_configuration.BuildConfiguration(build_configuration_dir + os.sep + rpath)
            build_configurations.append(bc)
            self.__logger.info('BuildConfiguration {0} loaded'.format(os.path.basename(bc.get_path_to_configuration_file())))
        return build_configurations


    def __create_top_generator(self, project_root_dir, codegen_dir, tbc, bcs):
        target_names = []
        for bc in bcs:
            target_names.append(bc.get_target_name())

        obj = top_generator.TopGenerator(
            tbc,
            project_root_dir,
            codegen_dir,
            target_names,
        )
        return obj


    def __create_specific_generators(self, project_root_dir, codegen_dir, papyrusrt_root_dir, bcs):
        list_target_names = []
        dict_specific_generators = {}

        for bc in bcs:
            obj = target_specific_generator.TargetSpecificGenerator(
                bc,
                project_root_dir,
                codegen_dir,
                papyrusrt_root_dir,
            )

            list_target_names.append(bc.get_target_name())
            dict_specific_generators[bc.get_target_name()] = obj

        return list_target_names, dict_specific_generators


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
