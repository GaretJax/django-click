import locale
import codecs

import six

import pytest

import click

from django.core.management import get_commands, call_command
from django.core.management import execute_from_command_line

import djclick


todo = pytest.mark.xfail(reason='TODO')


@pytest.mark.skipif(not six.PY3, reason='Only necessary on Python3')
def test_not_ascii():
    """
    Make sure that the systems preferred encoding is not `ascii`.

    Otherwise `click` is raising a RuntimeError for Python3. For a detailed
    description of this very problem please consult the following gist:
    https://gist.github.com/hackebrot/937245251887197ef542

    This test also checks that `tox.ini` explicitly copies the according
    system environment variables to the test environments.
    """
    try:
        preferred_encoding = locale.getpreferredencoding()
        fs_enc = codecs.lookup(preferred_encoding).name
    except Exception:
        fs_enc = 'ascii'
    assert fs_enc != 'ascii'


def test_attributes():
    for attr in click.__all__:
        assert hasattr(djclick, attr)


def test_command_recognized():
    assert 'testcmd' in get_commands()


def test_call_cli():
    execute_from_command_line(['./manage.py', 'testcmd'])
    with pytest.raises(RuntimeError):
        execute_from_command_line(['./manage.py', 'testcmd', '--raise'])


def test_call_command_args():
    call_command('testcmd')
    with pytest.raises(RuntimeError):
        call_command('testcmd', '--raise')


def test_call_command_kwargs():
    call_command('testcmd', raise_when_called=False)
    with pytest.raises(RuntimeError):
        call_command('testcmd', raise_when_called=True)


def test_call_command_kwargs_rename():
    call_command('testcmd', **{'raise': False})
    with pytest.raises(RuntimeError):
        call_command('testcmd', **{'raise': True})


def test_call_directly():
    from testapp.management.commands.testcmd import command

    command(raise_when_called=False)

    with pytest.raises(RuntimeError):
        command(raise_when_called=True)

    with pytest.raises(RuntimeError):
        command(**{'raise': True})


@todo
def test_django_verbosity():
    assert False


@todo
def test_django_pythonpath():
    assert False


@todo
def test_django_traceback():
    assert False


def test_django_settings(manage):
    # The --settings switch only works from the command line (or if the django
    # settings where not setup before... this means that we have to call it
    # in a subprocess.
    cmd = 'settingscmd'
    assert manage(cmd) == b'default'
    assert manage(cmd, '--settings', 'testprj.settings') == b'default'
    assert manage(cmd, '--settings', 'testprj.settings_alt') == b'alternative'


def test_django_color(capsys):
    call_command('colorcmd')
    out, err = capsys.readouterr()
    # Not passing a --color/--no-color flag defaults to autodetection. As the
    # command is run through the test suite, the autodetection defaults to
    # --no-color
    assert out == 'stdout'
    assert err == 'stderr'

    call_command('colorcmd', '--color')
    out, err = capsys.readouterr()
    assert out == click.style('stdout', fg='blue')
    assert err == click.style('stderr', bg='red')

    call_command('colorcmd', '--no-color')
    out, err = capsys.readouterr()
    assert out == 'stdout'
    assert err == 'stderr'


def test_django_help(manage):
    # The -h/--help switches cause the program to exit. Invoking the command
    # through execute_from_command_line would cause the test suit to exit as
    # well... this means that we have to call it in a subprocess.
    helps = [
        manage('helpcmd', '-h'),
        manage('helpcmd', '--help'),
        manage('help', 'helpcmd'),
    ]
    assert len(set(helps)) == 1

    help_text = helps[0]
    assert b'HELP_CALLED' not in help_text
    assert help_text.startswith(b'Usage: manage.py helpcmd ')


@todo
def test_django_version():
    assert False
