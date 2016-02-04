from django.core.exceptions import ObjectDoesNotExist

import djclick as click
from djclick.params import ModelInstance

from testapp.models import DummyModel


class DummyQuerySet(object):
    model = DummyModel

    def __init__(self, pk):
        self.pk = pk

    def get(self, pk):
        if pk == self.pk:
            return pk
        else:
            raise ObjectDoesNotExist()


@click.command()
@click.argument('instance', type=ModelInstance(DummyQuerySet('MODEL')))
def command(instance):
    # Just print some things which shall not be found in the output
    click.echo(instance, nl=False)
