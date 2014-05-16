:mod:`gs.recipe.base` API Reference
===================================

Currently this module only supplies the
:class:`gs.recipe.base.Recipe` **abstract** base class.

.. autoclass:: gs.recipe.base.Recipe
   :members: install, update, should_run, mark_locked


Example
-------

In the following example the **concrete** class ``SetupGSRecipe``
implements the ``install`` method. It calls ``should_run`` to
determine if the recipe should be run at all, and
calls ``mark_locked`` once it is done.

.. code-block:: python

    from gs.recipe.base import Recipe


    class SetupGSRecipe(Recipe):

       def get_script_command(self):
           'Get the command to do stuff'

        def install(self):
            if self.should_run():
                command = self.get_script_command()
                try:
                    retcode = subprocess.call(command, shell=True)
                    if retcode == 0:
                        self.mark_locked()
                        sys.stdout.write('GroupServer site created\n\n')
                    else:
                        m = '{0}: Issue running\n\t{1}\nReturned {2}\n'
                        msg = m.format(self.name, command, retcode)
                        raise UserError(msg)
                except OSError as e:
                    m = '{0}: Failed to run\n\t{1}\n{2}\n'
                    msg = m.format(self.name, command, e)
                    raise UserError(msg)

        return tuple()

    def update(self):
        self.install()
            
