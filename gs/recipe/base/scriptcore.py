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
    '''Recipe **abstract** base class.

:param dict buildout: The buildout options.
:param str name: The name of the recipe.
:param dict options: The recipe options.
:raises ValueError: If ``buildout['buildout']`` is missing
:raises ValueError: If ``buildout['buildout']['directory']`` is missing
:raises ValueError: If ``buildout['buildout']['bin-directory']`` is missing

Normally :mod:`zc.buildout` handles passing the correct values to ``buildout``,
``name``, and ``options``. As a result conformance is not as hard as it looks
from the signature of the ``__init__``.

**Concrete** implementations of this base class must implement the
:meth:`.install` method, and the :meth:`.update` method.
'''
    __metaclass__ = ABCMeta

    def __init__(self, buildout, name, options):
        if 'buildout' not in buildout:
            m = '"buildout" options absent from "buildout" dictionary.'
            raise ValueError(m)
        if 'directory' not in buildout['buildout']:
            m = '"directory" value not in the "buildout" options'
            raise ValueError(m)
        if 'bin-directory' not in buildout['buildout']:
            m = '"bin-directory" value not in the "buildout" options'
            raise ValueError(m)
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

The setup script {0} has already been run. To run
it again set the "run-once" option to "false", or delete
the file
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
        '''Determine if the recipe should be run.

:returns: ``True`` if the recipe should be run, ``False`` otherwise.
:rtype: ``bool``

A recipe should be run in two possible scenarios.

#.  The ``run-once`` buildout option is set to false, off, or no.
#.  The ``run-once`` is absent — or set to any value other than false, off or
    no — and the lock-file that is created by the :meth:`.mark_locked` method
    is absent.

As a **side** **effect,** a message is displayed to :data:`sys.stdout` if
:meth:`should_run` returns ``False``. This message tells the administrator how
to force the recipe to be run.
'''
        retval = True  # Uncharactistic optomisim
        if self.runonce:
            if os.path.exists(self.fileName):
                self.display_skipped_message()
                retval = False
        assert type(retval) == bool
        return retval

    def mark_locked(self):
        '''Create a lock file for the recipe.

:returns: ``None``

A lock-file is used to record that a recipe has already been run, and it
should be skipped. The presence or absence of the fille is important, rather
than the contents of the file.
'''
        with codecs.open(self.fileName, mode='w', encoding=UTF8) as lockfile:
            m = '''The presence of this file stops the setup script "{0}" from
being run more than once. Delete this file and run buildout to run the
setup script again.\n'''
            msg = m.format(self.name)
            lockfile.write(msg)

    @abstractmethod
    def install(self):
        '''A **concrete** implementation of this method should call the
following.

* :meth:`.should_run` to determine if the recipe should run at all.
* :meth:`.mark_locked` to lock the recipe after it has run.
'''

    @abstractmethod
    def update(self):
        '''Update the component, to be filled out by **concrete**
implementations.'''
