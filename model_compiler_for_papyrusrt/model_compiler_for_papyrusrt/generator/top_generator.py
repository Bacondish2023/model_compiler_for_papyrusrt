#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import logging

import model_compiler_for_papyrusrt.build_configuration.top_build_configuration as top_build_configuration
import model_compiler_for_papyrusrt.generator.top_cmakelists_generator as top_cmakelists_generator


class TopGenerator:


    def __init__(self, configuration, project_root_dir, codegen_dir, target_names):
        '''
        @brief Constructor
        @param[in] configuration instance of TopBuildConfiguration
        @param[in] project_root_dir path to project root directory
        @param[in] codegen_dir path to codegen directory
        @param[in] target_names list of targets. list of str type.
        '''
        # init logging
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__configuration = configuration
        self.__project_root_dir = project_root_dir
        self.__codegen_dir = codegen_dir
        self.__target_names = target_names


    def generateIfRequired(self):
        path_to_cmakelists = self.__codegen_dir + os.sep + 'CMakeLists.txt'
        path_to_configuration_file = self.__configuration.get_path_to_configuration_file()

        isRequired = False
        if os.path.isfile(path_to_cmakelists):
            if os.path.getmtime(path_to_cmakelists) < os.path.getmtime(path_to_configuration_file):
                isRequired = True
            else:
                isRequired = False
        else:
            isRequired = True

        if isRequired:
            self._generate()
        else:
            # nothing to do
            self.__logger.info('Skip to generate {0}'.format('CMakeLists.txt which corresponds to TopBuildConfiguration'))


    def _generate(self):
        cmakelists_gen = top_cmakelists_generator.TopCMakeListsGenerator(
            self.__codegen_dir,
            self.__target_names,
        )
        cmakelists_gen.generate()


if __name__ == '__main__':
    # executed
    pass
else:
    # imported
    pass
