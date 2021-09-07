"""
Support click in Django management commands.
"""

import click
from click import *  # NOQA
from .adapter import CommandRegistrator as command  # NOQA
from .adapter import GroupRegistrator as group, pass_verbosity  # NOQA

# The RegEx in setup.py requires single quotes. Rather than change it, turn off Black.
# fmt: off
__version__ = '2.3.0'
__url__ = 'https://github.com/GaretJax/django-click'
__author__ = 'Jonathan Stoppani'
__email__ = 'jonathan@stoppani.name'
__license__ = 'MIT'
# fmt: on

del click
