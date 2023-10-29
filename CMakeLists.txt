cmake_minimum_required(VERSION 3.17) # "rm" in CMake Command-Line Tool
project(Example)

##################################################
# platform settings
##################################################
if (IS_DIRECTORY $ENV{PAPYRUSRT_ROOT})
    message(STATUS "PAPYRUSRT_ROOT is \"$ENV{PAPYRUSRT_ROOT}\"")
else ()
    message(FATAL_ERROR "Directory \"$ENV{PAPYRUSRT_ROOT}\" which is specified by environment variable PAPYRUSRT_ROOT does not exist")
endif ()

if (UNIX)
    #add_definitions("-Wall")
elseif (MSVC)
    add_definitions("/source-charset:utf-8")
    #add_definitions("/Wall")
else ()
    message(FATAL_ERROR "Unknown platform")
endif ()

##################################################
# build rts
##################################################
include(libumlrts.cmake)

##################################################
# target for codegen
##################################################
add_custom_target(model_compile
    COMMAND
        python -B
        -m model_compiler_for_papyrusrt
        --loglevel INFO
        "${CMAKE_SOURCE_DIR}"
        "${CMAKE_SOURCE_DIR}/zzz_codegen"
        "${CMAKE_SOURCE_DIR}/build_configuration/top_build_configuration.xml"
    WORKING_DIRECTORY
        "${CMAKE_SOURCE_DIR}/model_compiler_for_papyrusrt"
)

##################################################
# build application
##################################################
add_subdirectory(zzz_codegen)
