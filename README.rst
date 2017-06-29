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

.. image:: https://img.shields.io/travis/GaretJax/django-click.svg
   :target: https://travis-ci.org/GaretJax/django-click

.. image:: https://img.shields.io/coveralls/GaretJax/django-click/master.svg
   :target: https://coveralls.io/r/GaretJax/django-click?branch=master

.. image:: https://img.shields.io/codeclimate/github/GaretJax/django-click.svg
   :target: https://codeclimate.com/github/GaretJax/django-click

.. image:: https://img.shields.io/requires/github/GaretJax/django-click.svg
   :target: https://requires.io/github/GaretJax/django-click/requirements/?branch=master

``django-click`` is a library to easily write Django management commands using the
``click`` command line library.

* Free software: MIT license
* Documentation for the Click command line library: http://click.pocoo.org/6/
* Compatible with Django 1.8, 1.10, and 1.11, running on Python 2.7, 3.4, 3.5, 3.6 and PyPy.


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
