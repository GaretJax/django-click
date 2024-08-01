============
Django Click
============

Project information:

.. image:: https://img.shields.io/pypi/v/django-click.svg
   :target: https://pypi.python.org/pypi/django-click

.. image:: https://img.shields.io/pypi/dm/django-click.svg
   :target: https://pypi.python.org/pypi/django-click

.. image:: https://img.shields.io/badge/docs-TODO-lightgrey.svg
   :target: http://django-click.readthedocs.org/en/latest/

.. image:: https://img.shields.io/pypi/l/django-click.svg
   :target: https://github.com/GaretJax/django-click/blob/master/LICENSE

Automated code metrics:

.. image:: https://img.shields.io/coveralls/GaretJax/django-click/master.svg
   :target: https://coveralls.io/r/GaretJax/django-click?branch=master

``django-click`` is a library to easily write Django management commands using the
``click`` command line library.

* Free software: MIT license
* Documentation for the Click command line library: https://click.palletsprojects.com/en/8.0.x/
* Compatible with Django 4.2 and 5.0 running on Python 3.8, 3.9, 3.10, 3.11, and 3.12 (note: 3.10+ required for Django 5.0).


Installation
============

::

  pip install django-click


Example
=======

Create a command module as you would usually do, but instead of creating a
class, just put a ``djclick`` command into
``<yourapp>/management/commands/helloworld.py``:

.. code:: python

   import djclick as click

   @click.command()
   @click.argument('name')
   def command(name):
       click.secho('Hello, {}'.format(name), fg='red')

And then call the command with::

   $ ./manage.py helloworld django-click
   Hello, django-click

Check out the `test commands
<https://github.com/GaretJax/django-click/tree/master/djclick/test/testprj/testapp/management/commands>`_
for additional example commands and advanced usage.

Release Notes and Contributors
==============================

* `Release Notes on GitHub <https://github.com/GaretJax/django-click/releases>`_
* `Our Wonderful Contributors <https://github.com/GaretJax/django-click/graphs/contributors>`_

This package is maintained by `Jonathan Stoppani <https://github.com/GaretJax/>`_ and `Timothy Allen <https://github.com/FlipperPA/>`_, who have many professional responsibilities. We are thrilled that our employers allow us a certain amount of time to contribute to open-source projects. We add features as they are necessary for our projects, and try to keep up with Issues and Pull Requests as best we can. Due to constraints of time (our full time jobs!), Feature Requests without a Pull Request may not be implemented, but we are always open to new ideas and grateful for contributions and our users.
