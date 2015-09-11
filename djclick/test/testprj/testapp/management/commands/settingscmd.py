import djclick as click

from django.conf import settings


@click.command()
def command():
    click.echo(settings.SETTINGS_NAME, nl=False)
