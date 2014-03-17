#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name = 'server_roles_poc',
    version = '0.0.1',
    description='D-BUS API for server roles',
    long_description='D-BUS API for server roles. Proof of Concept',
    keywords='fedora, dbus, server, server_roles',
    author='Stephen Gallagher',
    author_email='sgallagh@redhat.com',
    license = 'GPLv2',
    packages = find_packages(),
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                  ]
)
