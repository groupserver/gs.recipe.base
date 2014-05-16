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
from __future__ import absolute_import, unicode_literals
from abc import abstractmethod, ABCMeta
import codecs
import os
import sys
UTF8 = 'utf-8'


class Recipe(object):
    'Recipe **Abstract Base Class**'
    __metaclass__ = ABCMeta

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        configFile = "{0}.cfg".format(self.name)
        self.fileName = os.path.join(self.buildout['buildout']['directory'],
                                     'var', configFile)

        # suppress script generation
        self.options['scripts'] = ''
        self.options['bin-directory'] = buildout['buildout']['bin-directory']

    def display_skipped_message(self):
        'Display the message that the installation recipe has been skipped.'
        m = '''
------------------------------------------------------------

*Skipped* *{0}*

The setup script {0} has already been run. To run it again
set the "run-once" option to "false", or delete the file
{1}

------------------------------------------------------------\n\n'''
        msg = m.format(self.name, self.fileName)
        sys.stdout.write(msg)

    @property
    def runonce(self):
        '''Get the "run-once" value from the options.

:returns: The ``run-once`` value from the options, or ``true`` otherwise.
:rtype: ``bool``.

If the "run-once" value in the options is set to ``false``, ``off``, or ``no``
(regardless of case) then this will return ``False``. All other values, and
the absence of the "run-once" option, are interpreted as being ``True``.
'''
        runonce = ((('run-once' in self.options)
                    and self.options['run-once'].lower()) or 'true')
        retval = runonce not in ['false', 'off', 'no']
        assert type(retval) == bool
        return retval

    def should_run(self):
        'Determine if the recipe should be run.'
        retval = True  # Uncharactistic optomisim
        if self.runonce:
            if os.path.exists(self.fileName):
                self.display_skipped_message()
                retval = False
        return retval

    def mark_locked(self):
        'Mark the '
        with codecs.open(self.fileName, mode='w', encoding=UTF8) as lockfile:
            m = '''The presence of this file stops the setup script "{0}" from
being run more than once. Delete this file and run buildout to run the
setup script again.\n'''
            msg = m.format(self.name)
            lockfile.write(msg)

    @abstractmethod
    def install(self):
        '''Install the component.

A concrete class should call

* :meth:`should_run` to determine if the installer should run at all.
* :meth:`mark_locked` to lock the script after it has run.'''

    @abstractmethod
    def update(self):
        'Update the component'
