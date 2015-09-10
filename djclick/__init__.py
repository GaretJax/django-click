"""
Support click in Django management commands.
"""

import click
from click import *  # NOQA
from .adapter import CommandRegistrator


__version__ = '0.1.0'
__url__ = 'https://github.com/GaretJax/django-click'
__all__ = click.__all__

command = CommandRegistrator
