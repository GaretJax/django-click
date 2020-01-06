import os
import sys
from functools import update_wrapper

import six

import click

from django import get_version, VERSION as DJANGO_VERSION
from django.core.management import CommandError


class OptionParseAdapter(object):
    def parse_args(self, args):
        return (self, None)


class ArgumentParserDefaults(object):
    def __init__(self, args):
        self._args = args

    def _get_kwargs(self):
        return {
            'args': self._args,
        }


class ArgumentParserAdapter(object):
    def __init__(self):
        self._actions = []
        self._mutually_exclusive_groups = []

    def parse_args(self, args):
        return ArgumentParserDefaults(args)


class DjangoCommandMixin(object):
    use_argparse = False
    option_list = []
    base_stealth_options = []

    @property
    def stealth_options(self):
        return sum(
            ([p.name] + [i.lstrip('-') for i in p.opts] for p in self.params),
            [],
        )

    def invoke(self, ctx):
        try:
            return super(DjangoCommandMixin, self).invoke(ctx)
        except CommandError as e:
            # Honor the --traceback flag
            if ctx.traceback:
                raise
            styled_message = click.style('{}: {}'.format(e.__class__.__name__, e), fg='red', bold=True)
            click.echo(styled_message, err=True)
            ctx.exit(1)

    def run_from_argv(self, argv):
        """
        Called when run from the command line.
        """
        prog_name = '{} {}'.format(os.path.basename(argv[0]), argv[1])
        try:
            # We won't get an exception here in standalone_mode=False
            exit_code = self.main(args=argv[2:], prog_name=prog_name, standalone_mode=False)
            if exit_code:
                sys.exit(exit_code)
        except click.ClickException as e:
            if hasattr(e, 'ctx') and getattr(e.ctx, 'traceback', False):
                raise
            e.show()
            sys.exit(e.exit_code)

    def create_parser(self, progname, subcommand):
        """
        Called when run through `call_command`.
        """
        if DJANGO_VERSION >= (1, 10):
            return ArgumentParserAdapter()
        else:
            return OptionParseAdapter()

    def print_help(self, prog_name, subcommand):
        prog_name = '{} {}'.format(prog_name, subcommand)
        self.main(['--help'], prog_name=prog_name, standalone_mode=False)

    def map_names(self):
        for param in self.params:
            for opt in param.opts:
                yield opt.lstrip('--').replace('-', '_'), param.name

    def execute(self, *args, **kwargs):
        """
        Called when run through `call_command`. `args` are passed through,
        while `kwargs` is the __dict__ of the return value of
        `self.create_parser('', name)` updated with the kwargs passed to
        `call_command`.
        """
        # Remove internal Django command handling machinery
        kwargs.pop('skip_checks', None)
        parent_ctx = click.get_current_context(silent=True)
        with self.make_context('', list(args), parent=parent_ctx) as ctx:
            # Rename kwargs to to the appropriate destination argument name
            opt_mapping = dict(self.map_names())
            arg_options = {opt_mapping.get(key, key): value
                           for key, value in six.iteritems(kwargs)}

            # Update the context with the passed (renamed) kwargs
            ctx.params.update(arg_options)

            # Invoke the command
            self.invoke(ctx)

    def __call__(self, *args, **kwargs):
        """
        When invoked, normal click commands act as entry points for command
        line execution. When using Django, commands get invoked either through
        the `execute_from_command_line` or `call_command` utilities.

        Calling a command directly can thus be just a shortcut for calling its
        `execute` method.
        """
        return self.execute(*args, **kwargs)


class CommandAdapter(DjangoCommandMixin, click.Command):
    pass


class GroupAdapter(DjangoCommandMixin, click.Group):
    pass


def register_on_context(ctx, param, value):
    setattr(ctx, param.name, value)
    return value


def suppress_colors(ctx, param, value):
    # Only set the value if a flag was provided, otherwise we would override
    # the default set by the parent context if one was available.
    if value is not None:
        ctx.color = value
    return value


class BaseRegistrator(object):
    common_options = [
        click.option(
            '-v', '--verbosity',
            expose_value=False,
            default='1',
            callback=register_on_context,
            type=click.IntRange(min=0, max=3),
            help=('Verbosity level; 0=minimal output, 1=normal ''output, '
                  '2=verbose output, 3=very verbose output.'),
        ),
        click.option(
            '--settings',
            metavar='SETTINGS',
            expose_value=False,
            help=('The Python path to a settings module, e.g. '
                  '"myproject.settings.main". If this is not provided, the '
                  'DJANGO_SETTINGS_MODULE environment variable will be used.'),
        ),
        click.option(
            '--pythonpath',
            metavar='PYTHONPATH',
            expose_value=False,
            help=('A directory to add to the Python path, e.g. '
                  '"/home/djangoprojects/myproject".'),
        ),
        click.option(
            '--traceback/--no-traceback',
            is_flag=True,
            default=False,
            expose_value=False,
            callback=register_on_context,
            help='Raise on CommandError exceptions.',
        ),
        click.option(
            '--color/--no-color',
            default=None,
            expose_value=False,
            callback=suppress_colors,
            help=('Enable or disable output colorization. Default is to '
                  'autodetect the best behavior.'),
        ),
    ]

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.version = self.kwargs.pop('version', get_version())

        context_settings = kwargs.setdefault('context_settings', {})
        context_settings['help_option_names'] = ['-h', '--help']

    def get_params(self, name):
        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                click.echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return [
            click.version_option(version=self.version, message='%(version)s'),
            click.option('-h', '--help', is_flag=True, is_eager=True,
                         expose_value=False, callback=show_help,
                         help='Show this message and exit.',),
        ] + self.common_options

    def __call__(self, func):
        module = sys.modules[func.__module__]

        # Get the command name as Django expects it
        self.name = func.__module__.rsplit('.', 1)[-1]

        # Build the click command
        decorators = [
            click.command(name=self.name, cls=self.cls, **self.kwargs),
        ] + self.get_params(self.name)

        for decorator in reversed(decorators):
            func = decorator(func)

        # Django expects the command to be callable (it instantiates the class
        # pointed at by the `Command` module-level property)...
        # ...let's make it happy.
        module.Command = lambda: func

        return func


def pass_verbosity(f):
    """
    Marks a callback as wanting to receive the verbosity as a keyword argument.
    """
    def new_func(*args, **kwargs):
        kwargs['verbosity'] = click.get_current_context().verbosity
        return f(*args, **kwargs)
    return update_wrapper(new_func, f)


class CommandRegistrator(BaseRegistrator):
    cls = CommandAdapter


class GroupRegistrator(BaseRegistrator):
    cls = GroupAdapter
