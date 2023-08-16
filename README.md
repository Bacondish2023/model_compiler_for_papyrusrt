# Model Compiler for Papyrus-RT

## Introduction

**Model Compiler for Papyrus-RT** is a build tool for projects which use Papyrus-RT.
It enables command-line code generation and build and works on various platforms.

The Model Compiler for Papyrus-RT supports **BuildConfiguration** file
which has codegen, build settings.
This feature makes development with CI tool such as Jenkins easy.

TODO place concept drawing here

The Model Compiler for Papyrus-RT inputs model and BuildConfiguration.
And it generates source codes and CMake build scripts.
(Codegen functionality uses Papyrus-RT's standalone code generator.)

## Motivation

Papyrus for Real Time (Papyrus-RT) is a UMR-RT based software development tool.
User can do modeling and generate code with Papyrus-RT to develop software.
The latest(1.0.0) one does not support command-line code generation officially.
And unfortunately Papyrus-RT development seems to be not active.

I hope that there is command-line code generation feature on Papyrus-RT for development with CI tool such as Jenkins.

## Features

* Command-line code generation
* Build configuration support
* Platform-independent

## Prerequisites

#### Supported Platform

* Linux
* Windows(MSVC)

#### Required Software

* **Papyrus-RT**
* **Python 3** 3.6.8 or above
* **CMake** 3.17 or above
* And toolchain which can build C++ source code

## How to Use

Under construction

## Directory Structure

Under construction

## License

Copyright 2023 [Hidekazu TAKAHASHI](https://github.com/Bacondish2023).
The Model Compiler for Papyrus-RT is free and open-source software licensed
under the **Eclipse Public License 1.0**.

The Model Compiler for Papyrus-RT includes following derived work.

 * **papyrusrt_codegen_wrapper.py** is derived from
   **umlrtgen.sh** which is available in the Papyrus-RT and licensed under the EPL 1.0.
