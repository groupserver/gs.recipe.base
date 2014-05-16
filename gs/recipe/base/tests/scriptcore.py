# -*- coding: utf-8 -*-
import mock
from os import mkdir
from os.path import exists
from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase
import gs.recipe.base.scriptcore


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
        self.recipe = gs.recipe.base.scriptcore.Recipe(self.buildout,
                                                    self.name, self.options)

        gs.recipe.base.scriptcore.sys.stdout = mock.MagicMock()
        gs.recipe.base.scriptcore.sys.stderr = mock.MagicMock()

    def tearDown(self):
        rmtree(self.tempdir)

    def test_display_skipped_message(self):
        self.recipe.display_skipped_message()
        args, kw_args = gs.recipe.base.scriptcore.sys.stdout.write.call_args
        msg = args[0]
        self.assertIn(self.name, msg)
        self.assertIn(self.tempdir, msg)

    def should_run_false_options(self, val):
        '''Test if seting the "run-once" option to false always causes
        the should_run method to return True.'''
        self.recipe.options = {'run-once': val}
        with open(self.recipe.fileName, 'w') as togglefile:
            togglefile.write('1')
        r = self.recipe.should_run()
        self.assertTrue(r)

    def _test_should_run_false(self):
        'Test if setting run-once to False prevents the script from being run'
        self.should_run_false_options('false')
        self.should_run_false_options('False')

    def _test_should_run_no(self):
        'Test if setting run-once to No prevents the script from being run'
        self.should_run_false_options('no')
        self.should_run_false_options('No')

    def _test_should_run_off(self):
        'Test if setting run-once to Off prevents the script from being run'
        self.should_run_false_options('off')
        self.should_run_false_options('Off')

    def _test_should_run_no_file(self):
        '''Test if should_run returns True if there is no toggle-file'''
        r = self.recipe.should_run()
        self.assertTrue(r)

    def _test_should_run_file(self):
        '''Test if should_run returns False if there is a toggle-file'''
        with open(self.recipe.fileName, 'w') as togglefile:
            togglefile.write('1')
        r = self.recipe.should_run()
        self.assertFalse(r)
