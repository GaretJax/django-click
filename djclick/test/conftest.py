from io import BytesIO
import os
import subprocess
import sys

import pytest


@pytest.fixture(scope='session')
def manage():
    def call(*args):
        cmd = [
            sys.executable,
            os.path.join(os.path.dirname(__file__), 'testprj', 'manage.py'),
        ] + list(args)
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    return call


@pytest.fixture
def call_command():
    from django.core.management import call_command

    class CallCommand(object):
        def __init__(self):
            self.io = BytesIO()

        def __call__(self, *args, **kwargs):
            self.io = BytesIO()
            stdout = sys.stdout
            try:
                sys.stdout = self.io
                call_command(*args, **kwargs)
            finally:
                sys.stdout = stdout
            return self

        @property
        def stdout(self):
            return self.io.getvalue()

    return CallCommand()
