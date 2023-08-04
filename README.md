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
* Windows
* Mac OS? (not tested)

#### Required Software

* Papyrus-RT
* CMake
* Python 3

## How to Use

Under construction

## Directory Structure

Under construction

## License

Under construction
