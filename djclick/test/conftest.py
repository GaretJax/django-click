import sys
import os
import contextlib
import subprocess

import pytest


@contextlib.contextmanager
def set_key(dictionary, key, value):
    key_is_set = key in dictionary
    original_value = dictionary.pop(key, None)

    dictionary[key] = value

    try:
        yield
    finally:
        if key_is_set:
            dictionary[key] = original_value
        else:
            del dictionary[key]


@contextlib.contextmanager
def insert_value(list, index, value):
    list.insert(index, value)
    try:
        yield
    finally:
        if value in list:
            list.pop(list.index(value))


@pytest.yield_fixture(autouse=True, scope='session')
def test_project():
    project_dir = os.path.join(os.path.dirname(__file__), 'testprj')
    with insert_value(sys.path, 0, project_dir):
        with set_key(os.environ, 'DJANGO_SETTINGS_MODULE', 'testprj.settings'):
            from django.conf import settings
            assert 'testapp' in settings.INSTALLED_APPS

            import django
            if hasattr(django, 'setup'):
                django.setup()

            yield


@pytest.fixture(scope='session')
def manage():
    def call(*args):
        cmd = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), 'testprj', 'manage.py'),
        ] + list(args)
        return subprocess.check_output(cmd)

    return call
