# -*- coding: utf-8 -*-
import codecs
from mock import MagicMock
from os import mkdir
from os.path import exists
from random import shuffle
from shutil import rmtree
from string import ascii_letters
from tempfile import mkdtemp
from unittest import TestCase
import gs.recipe.base.scriptcore
UTF8 = 'utf-8'


class FauxRecipe(gs.recipe.base.scriptcore.Recipe):
    '''Ce n'est pas un Recipe.'''

    def install(self):
        "Ce n'est pas un install'"

    def update(self):
        "Ce n'est pas un update'"


class TestRecipe(TestCase):
    'Test the core of the recipes'

    def setUp(self):
        self.tempdir = mkdtemp()
        self.bindir = '{0}/bin'.format(self.tempdir)
        mkdir(self.bindir)
        vardir = '{0}/var'.format(self.tempdir)
        mkdir(vardir)

        self.buildout = {'buildout': {'directory': self.tempdir,
                                        'bin-directory': self.bindir, }, }
        self.name = 'setupgs'
        self.options = {}
        self.options['recipe'] = 'gs.recipe.base'
        self.options['zope_admin_name'] = 'dug'
        self.options['zope_admin'] = 'parannah'
        self.options['instance_id'] = 'ethel_the_frog'
        self.options['instance_title'] = 'violence in british gangland'
        self.options['support_email'] = 'support@example.comd'
        self.options['gs_admin_email'] = 'dug@example.com'
        self.options['gs_admin_password'] = 'toad the wet sprocket'
        self.options['gs_host'] = 'groups.example.com'
        self.options['gs_port'] = '42'
        self.options['gs_smtp_host'] = 'smtp.example.com'
        self.options['gs_smtp_port'] = '42'
        self.options['gs_smtp_user'] = ''
        self.options['gs_smtp_password'] = ''

        # Use a concrete class, rather than the ABC
        self.recipe = FauxRecipe(self.buildout, self.name, self.options)

        gs.recipe.base.scriptcore.sys.stdout = MagicMock()
        gs.recipe.base.scriptcore.sys.stderr = MagicMock()

    def tearDown(self):
        rmtree(self.tempdir)

    def display_message_test(self):
        'Tests for the Skipped message'
        args, kw_args = gs.recipe.base.scriptcore.sys.stdout.write.call_args
        msg = args[0]
        self.assertIn(self.name, msg)
        self.assertIn(self.tempdir, msg)

    def test_display_skipped_message(self):
        'Test that the "skipped" message has the name of the script'
        self.recipe.display_skipped_message()
        self.display_message_test()

    def runonce_false_options(self, val):
        '''Test if seting the "run-once" option to false always causes
        the should_run method to return True.'''
        self.recipe.options = {'run-once': val}
        r = self.recipe.runonce
        self.assertFalse(r)

    def test_runonce_false(self):
        'Test if setting run-once to False prevents the script from being run'
        self.runonce_false_options('false')
        self.runonce_false_options('False')

    def test_runonce_no(self):
        'Test if setting run-once to No prevents the script from being run'
        self.runonce_false_options('no')
        self.runonce_false_options('No')

    def test_runonce_off(self):
        'Test if setting run-once to Off prevents the script from being run'
        self.runonce_false_options('off')
        self.runonce_false_options('Off')

    @staticmethod
    def random_str():
        l = list(ascii_letters)
        shuffle(l)
        retval = ''.join(l)
        return retval

    def test_runonce_true(self):
        'Test if a "run-once" value of anything else evalueates to ``True``'
        val = self.random_str()[:7]  # Six letters so "False" cannot come up
        self.recipe.options = {'run-once': val}
        r = self.recipe.runonce
        self.assertTrue(r)

    def test_runonce_missing_true(self):
        'Test if a missing "run-once" value evalueates to ``True``'
        r = self.recipe.runonce
        self.assertTrue(r)

    def test_should_run_no_file(self):
        '''Test if should_run returns ``True`` if the toggle-file is absent'''
        r = self.recipe.should_run()
        self.assertTrue(r)

    def make_toggle_file(self):
        with codecs.open(self.recipe.fileName, 'w', UTF8) as togglefile:
            togglefile.write(self.random_str()[:15])

    def test_should_run_file(self):
        '''Test if should_run returns ``False`` if there is a toggle-file'''
        self.make_toggle_file()
        r = self.recipe.should_run()
        self.assertFalse(r)
        # Check that the Skipped message was displayed
        self.display_message_test()

    def test_should_run_file_runonce_false(self):
        '''``should_run`` should return ``True`` if run-once is ``False`` and
there is a toggle file'''
        self.make_toggle_file()
        self.recipe.options = {'run-once': 'False'}
        r = self.recipe.should_run()
        self.assertTrue(r)

    def test_mark_locked(self):
        'Test if ``mark_locked`` creates a lockfile'
        self.recipe.mark_locked()
        r = exists(self.recipe.fileName)
        self.assertTrue(r)
