from django.core.management import CommandError

import djclick as click


@click.command(version="20.0")
def command():
    raise CommandError("Raised error description")
