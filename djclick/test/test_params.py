from click.exceptions import BadParameter
import pytest

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
@pytest.mark.parametrize(
    ('arg', 'value'),
    (
        ('--pk', '1'),
        ('--slug', 'test'),
        ('--endswith', 'st'),
    )
)
def test_convert_ok(call_command, arg, value):
    from testapp.models import DummyModel

    DummyModel.objects.create(pk=1, slug='test')
    expected = b'<DummyModel: 1>'

    assert call_command('modelcmd', arg, value).stdout == expected


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('args', 'error_message'),
    (
        (('--pk', '99'), "pk=99"),
        (('--slug', 'doesnotexist'), "slug=doesnotexist"),
    )
)
def test_convert_fail(call_command, args, error_message):
    with pytest.raises(BadParameter) as e:
        call_command('modelcmd', *args)
    assert e.match(
        'could not find testapp.DummyModel with {}'.format(error_message))
