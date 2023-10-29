#!/bin/bash
#
# @file papyrusrt.sh
# @brief Launches papyrus on workspace
#

WORKSPACE_DIR=zzz_workspace

if [ ! -d "$WORKSPACE_DIR" ]; then
  mkdir $WORKSPACE_DIR
fi

papyrusrt -data $WORKSPACE_DIR &
