import pytest
from click.exceptions import BadParameter

from djclick import params


@pytest.mark.django_db
def test_modelinstance_init():
    from testapp.models import DummyModel
    from django.db.models.query import QuerySet

    param = params.ModelInstance(DummyModel)
    assert isinstance(param.qs, QuerySet)

    qs = DummyModel.objects.all()
    param = params.ModelInstance(qs)
    assert param.qs is qs


@pytest.mark.django_db
def test_convert_ok(call_command):
    from testapp.models import DummyModel

    DummyModel.objects.create()
    assert call_command('modelcmd', '1').stdout == b'1'


@pytest.mark.django_db
def test_convert_fail(call_command):
    with pytest.raises(BadParameter) as e:
        call_command('modelcmd', '999')
    # Use `.endswith()` because of differences between CPython and pypy
    assert str(e).endswith('BadParameter: could not find '
                           'testapp.DummyModel with pk=999')
