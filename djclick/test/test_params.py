import os
import subprocess

from djclick import params


def test_modelinstance_init():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testprj.settings')

    from testapp.models import DummyModel
    from django.db.models.query import QuerySet

    param = params.ModelInstance(DummyModel)
    assert isinstance(param.qs, QuerySet)

    qs = DummyModel.objects.all()
    param = params.ModelInstance(qs)
    assert param.qs is qs


def test_convert_ok(manage):
    assert manage('modelcmd', 'MODEL') == b'MODEL'


def test_convert_fail(manage):
    try:
        manage('modelcmd', 'ND')
    except subprocess.CalledProcessError as e:
        lines = e.output.strip().splitlines()
        assert b'Traceback (most recent call last):' == lines[0]
        for line in lines[1:-1]:
            assert line.startswith(b'  ')
        # Use `.endswith()` because of differences between CPython and pypy
        assert lines[-1].endswith(b'BadParameter: could not find '
                                  b'testapp.DummyModel with pk=ND')
        assert e.returncode == 1
    else:
        assert False  # NOCOV
