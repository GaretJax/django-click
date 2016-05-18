import djclick as click
from djclick.params import ModelInstance

from testapp.models import DummyModel


@click.command()
@click.argument('instance', type=ModelInstance(DummyModel.objects.all()))
def command(instance):
    # Just print some things which shall not be found in the output
    click.echo(instance, nl=False)
