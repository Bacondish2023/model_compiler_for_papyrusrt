#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

setup(  name = 'model_compiler_for_papyrusrt',
        version = '1.0.0',
        description = 'A build tool for projects using Papyrus-RT.',
        url='https://github.com/Bacondish2023/model_compiler_for_papyrusrt',
        author = 'Hidekazu TAKAHASHI',
        author_email = '139677991+Bacondish2023@users.noreply.github.com',
        license = 'Eclipse Public License 1.0',

        classifiers=[
            'Topic :: Software Development :: Build Tools',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
        ],

        keywords='development build-tool papyrusrt modeling',

        python_requires='>=3.6',

        packages = [
            'model_compiler_for_papyrusrt',
            'model_compiler_for_papyrusrt/build_configuration',
            'model_compiler_for_papyrusrt/generator',
            'model_compiler_for_papyrusrt/misc',
            ],
        )
