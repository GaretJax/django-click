import djclick as click
from djclick.params import ModelInstance

from testapp.models import DummyModel


@click.command()
@click.option("--pk", type=ModelInstance(DummyModel))
@click.option("--slug", type=ModelInstance(DummyModel, lookup="slug"))
@click.option("--endswith", type=ModelInstance(DummyModel, lookup="slug__endswith"))
def command(pk, slug, endswith):
    if pk:
        click.echo(repr(pk), nl=False)
    if slug:
        click.echo(repr(slug), nl=False)
    if endswith:
        click.echo(repr(endswith), nl=False)
