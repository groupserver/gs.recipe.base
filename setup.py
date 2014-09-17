# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.rst"), encoding='utf-8') as f:
    long_description += '\n' + f.read()

# The systems based on this will need to define an entry point:
# entry_point = 'gs.recipe.setupgs:Recipe'
# entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require = ['mock']

setup(name='gs.recipe.base',
      version=version,
      description="The core of the ``zc.buildout`` recipes for GroupServer",
      long_description=long_description,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Zope Public License',
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        ],
      keywords='zope, groupserver, recipe, setup, instance, install',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://source.iopen.net/groupserver/gs.recipe.base/',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require,
                          docs=['Sphinx', ]),
      test_suite='gs.recipe.base.tests.test_all',
#      entry_points=entry_points,
      )
