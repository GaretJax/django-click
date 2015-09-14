"""
Support click in Django management commands.
"""

import click
from click import *  # NOQA
from .adapter import CommandRegistrator as command  # NOQA
from .adapter import GroupRegistrator as group, pass_verbosity  # NOQA


__version__ = '0.1.1'
__url__ = 'https://github.com/GaretJax/django-click'
__all__ = click.__all__ + ['pass_verbosity']
