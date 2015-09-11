============
Django Click
============

.. image:: https://img.shields.io/travis/GaretJax/django-click.svg
   :target: https://travis-ci.org/GaretJax/django-click

.. image:: https://img.shields.io/pypi/v/django-click.svg
   :target: https://pypi.python.org/pypi/django-click

.. image:: https://img.shields.io/pypi/dm/django-click.svg
   :target: https://pypi.python.org/pypi/django-click

.. image:: https://img.shields.io/coveralls/GaretJax/django-click/master.svg
   :target: https://coveralls.io/r/GaretJax/django-click?branch=master

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://django-click.readthedocs.org/en/latest/

.. image:: https://img.shields.io/pypi/l/django-click.svg
   :target: https://github.com/GaretJax/django-click/blob/develop/LICENSE

.. image:: https://img.shields.io/requires/github/GaretJax/django-click.svg
   :target: https://requires.io/github/GaretJax/django-click/requirements/?branch=master

.. image:: https://img.shields.io/codeclimate/github/GaretJax/django-click.svg
   :target: https://codeclimate.com/github/GaretJax/django-click

django-click is a library to easily write django management commands using the
click command line library.

* Free software: MIT license
* Documentation: http://django-click.rtfd.org


Installation
============

::

  pip install django-click


Example
=======

Create a command module as you would usually do, but instead of creating a
class, just put a djclick command into it::

   import djclick as click

   @click.command()
   @click.argument('name')
   def command(name):
      click.secho('Hello, {}'.format(name), fg='red')
