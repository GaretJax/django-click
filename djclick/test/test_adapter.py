import os
import locale
import codecs
import subprocess

import six

import pytest

import click

import django
from django.core.management import get_commands, call_command
from django.core.management import execute_from_command_line

import djclick


todo = pytest.mark.xfail(reason='TODO')


@pytest.mark.skipif(not six.PY3, reason='Only necessary on Python3')
def test_not_ascii():  # NOCOV
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


def test_django_verbosity(capsys):
    # Make sure any command can be called, even if it does not explictly
    # accept the --verbosity option
    with pytest.raises(RuntimeError):
        execute_from_command_line([
            './manage.py', 'testcmd', '--raise', '--verbosity', '1'])

    # Default
    execute_from_command_line([
        './manage.py', 'ctxverbositycmd'])
    out, err = capsys.readouterr()
    assert out == '1'

    # Explicit
    execute_from_command_line([
        './manage.py', 'ctxverbositycmd', '--verbosity', '2'])
    out, err = capsys.readouterr()
    assert out == '2'

    # Invalid
    with pytest.raises(click.BadParameter):
        execute_from_command_line([
            './manage.py', 'ctxverbositycmd', '--verbosity', '4'])

    # Default (option)
    execute_from_command_line([
        './manage.py', 'argverbositycommand'])
    out, err = capsys.readouterr()
    assert out == '1'

    # Explicit (option)
    execute_from_command_line([
        './manage.py', 'argverbositycommand', '--verbosity', '2'])
    out, err = capsys.readouterr()
    assert out == '2'


def test_django_pythonpath(manage):
    with pytest.raises(subprocess.CalledProcessError):
        manage('pathcmd')

    manage('pathcmd', '--pythonpath',
           os.path.join(os.path.dirname(__file__), 'testdir')) == b'1'


def test_django_traceback(manage):
    try:
        manage('errcmd')
    except subprocess.CalledProcessError as e:
        assert e.output == b'CommandError: Raised error description\n'
        assert e.returncode == 1
    else:
        assert False  # NOCOV

    try:
        manage('errcmd', '--traceback')
    except subprocess.CalledProcessError as e:
        lines = e.output.splitlines()
        assert lines[0] == b'Traceback (most recent call last):'
        for line in lines[1:-1]:
            assert line.startswith(b'  ')
        # Use `.endswith()` because of differences between CPython and pypy
        assert lines[-1].endswith(b'CommandError: Raised error description')
        assert e.returncode == 1
    else:
        assert False  # NOCOV


def test_django_settings(manage):
    # The --settings switch only works from the command line (or if the django
    # settings where not setup before)... this means that we have to call it
    # in a subprocess.
    cmd = 'settingscmd'
    assert manage(cmd) == b'default'
    assert manage(cmd, '--settings', 'testprj.settings') == b'default'
    assert manage(cmd, '--settings', 'testprj.settings_alt') == b'alternative'


def test_django_color(capsys):
    call_command('colorcmd')
s    out, err = capsys.readouterr()
    # Not passing a --color/--no-color flag defaults to autodetection. As the
    # command is run through the test suite, the autodetection defaults to not
    # colorizing the output.
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


def test_django_version(manage):
    django_version = django.get_version().encode('ascii') + b'\n'
    if django.VERSION < (1, 8):
        prefix = django_version
    else:
        prefix = b''
    assert manage('testcmd', '--version') == prefix + django_version
    assert manage('versioncmd', '--version') == prefix + b'20.0\n'


def test_group_command(capsys):
    execute_from_command_line(['./manage.py', 'groupcmd'])
    out, err = capsys.readouterr()
    assert out == 'group_command\n'

    execute_from_command_line(['./manage.py', 'groupcmd', 'subcmd1'])
    out, err = capsys.readouterr()
    assert out == 'group_command\nSUB1\n'

    execute_from_command_line(['./manage.py', 'groupcmd', 'subcmd3'])
    out, err = capsys.readouterr()
    assert out == 'group_command\nSUB2\n'
