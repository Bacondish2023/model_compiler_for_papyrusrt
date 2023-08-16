# @brief Build script for Runtime Service(RTS) library
#
# Usage
# - Specify RTS source directory with environment variable UMLRTS_ROOT
# - Include this file (include() in CMake)
# - Link "libumlrts" to your executable (target_link_libraries() in CMake)
#     - RTS include directories are propagated with link
#       So, you don't have to wirte target_include_directories().
# - Specify RTS include directories to your library
#     - Write target_include_directories() with UMLRTS_INCLUDE_DIRS CMake variable
#
# Available variable
# - UMLRTS_INCLUDE_DIRS   RTS include directories
#
# Supported platforms
# - Linux
# - MSVC
#

if (IS_DIRECTORY $ENV{UMLRTS_ROOT})
    message(STATUS "UMLRTS_ROOT is \"$ENV{UMLRTS_ROOT}\"")

    set(UMLRTS_ROOT_NORMALIZED $ENV{UMLRTS_ROOT})
    string(REPLACE "\\" "/" UMLRTS_ROOT_NORMALIZED ${UMLRTS_ROOT_NORMALIZED})
    string(REPLACE "//" "/" UMLRTS_ROOT_NORMALIZED ${UMLRTS_ROOT_NORMALIZED})

    set(UMLRTS_INCLUDE_DIRS
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/src/include
        ${UMLRTS_ROOT_NORMALIZED}/include
        ${UMLRTS_ROOT_NORMALIZED}/util/include
    )

    add_library(libumlrts STATIC
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/src/umlrtgetopt.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtapi.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtbasicthread.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtcapsule.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtcapsuleid.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtcapsuletocontrollermap.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtcommsport.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtcontroller.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtframeprotocol.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtframeservice.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrthashmap.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtinsignal.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtinoutsignal.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtlogprotocol.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmain.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmainloop.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmaintargetshutdown.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmaintargetstartup.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmessage.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmessagepool.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtmessagequeue.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtobjectclass.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtoutsignal.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtpool.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtprioritymessagequeue.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtprotocol.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtqueue.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtrtsinterfaceumlrt.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtsignal.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtsignalelement.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrtsignalelementpool.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrttimerid.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrttimerpool.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrttimerprotocol.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrttimerqueue.cc
        ${UMLRTS_ROOT_NORMALIZED}/umlrt/umlrttimespec.cc
    )

    target_include_directories(
        libumlrts
        PUBLIC
            ${UMLRTS_INCLUDE_DIRS}
    )

    if (UNIX)
        target_sources(
            libumlrts
            PRIVATE
                ${UMLRTS_ROOT_NORMALIZED}/util/basedebug.cc
                ${UMLRTS_ROOT_NORMALIZED}/util/basefatal.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/osbasicthread.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/osmutex.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/osnotify.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/ossemaphore.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/ostime.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/ostimespec.cc
        )
        target_include_directories(
            libumlrts
            PUBLIC
                ${UMLRTS_ROOT_NORMALIZED}/os/linux/include
        )
    elseif (MSVC)
        target_compile_definitions(
            libumlrts
            PRIVATE
                /source-charset:utf-8
        )
        target_sources(
            libumlrts
            PRIVATE
                ${UMLRTS_ROOT_NORMALIZED}/util/basedebug.cc
                ${UMLRTS_ROOT_NORMALIZED}/util/basefatal.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/osbasicthread.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/osmutex.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/osnotify.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/ossemaphore.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/ostime.cc
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/ostimespec.cc
        )
        target_include_directories(
            libumlrts
            PUBLIC
                ${UMLRTS_ROOT_NORMALIZED}/os/windows/include
        )
    else ()
        message(FATAL_ERROR "Unknown platform")
    endif ()
else ()
    message(FATAL_ERROR "Directory \"$ENV{UMLRTS_ROOT}\" which is specified by environment variable UMLRTS_ROOT does not exist")
endif ()
