import sys

import six

import click

from django import get_version


class ParserAdapter(object):
    def parse_args(self, args):
        return (self, None)


class CommandAdapter(click.Command):
    use_argparse = False

    def run_from_argv(self, argv):
        """
        Called when run from the command line.
        """
        return self.main(args=argv[2:])

    def create_parser(self, progname, subcommand):
        """
        Called when run through `call_command`.
        """
        return ParserAdapter()

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
        kwargs.pop('skip_checks')

        with self.make_context('', list(args)) as ctx:
            # Rename kwargs to to the appropriate destination argument name
            opt_mapping = dict(self.map_names())
            arg_options = {opt_mapping.get(key, key): value
                           for key, value in six.iteritems(kwargs)}

            # Update the context with the passed (renamed) kwargs
            ctx.params.update(arg_options)

            # Invoke the command
            self.invoke(ctx)


def register_on_context(ctx, param, value):
    setattr(ctx, param.name, value)
    return value


def suppress_colors(ctx, param, value):
    if value:
        ctx.color = False
    return value


class CommandRegistrator(object):
    common_options = [
        click.option(
            '-v', '--verbosity',
            expose_value=False,
            callback=register_on_context,
            type=click.Choice(str(s) for s in range(4)),
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
            '--traceback',
            is_flag=True,
            expose_value=False,
            callback=register_on_context,
            help='Raise on CommandError exceptions.',
        ),
        click.option(
            '--no-color',
            is_flag=True,
            expose_value=False,
            callback=suppress_colors,
            help='Do not colorize the command output.',
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
                ctx.info_name += ' ' + name
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
            click.command(name=self.name, cls=CommandAdapter, **self.kwargs),
        ] + self.get_params(self.name)

        for decorator in reversed(decorators):
            func = decorator(func)

        # Django expects the command to be callable (it instantiates the class
        # pointed at by the `Command` module-level property)...
        # ...let's make it happy.
        module.Command = lambda: func

        return func
