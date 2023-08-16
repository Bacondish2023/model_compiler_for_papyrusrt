@echo off
rem
rem @file papyrusrt.bat
rem @brief Launches papyrus on workspace
rem

set WORKSPACE_DIR=zzz_workspace

if not exist "%WORKSPACE_DIR%\" (
  mkdir "%WORKSPACE_DIR%"
)

start papyrusrt.exe -data "%WORKSPACE_DIR%"
