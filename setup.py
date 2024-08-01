#!/usr/bin/env python

import io
import os
import re
import sys
import glob

from setuptools import setup, find_packages


PACKAGE = "djclick"
PACKAGE_NAME = "django-click"
DESCRIPTION = "Build Django management commands using the click CLI package."
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist bdist_wheel upload")
    sys.exit()


class Setup(object):
    @staticmethod
    def read(fname, fail_silently=False):
        """
        Read the content of the given file. The path is evaluated from the
        directory containing this file.
        """
        try:
            filepath = os.path.join(os.path.dirname(__file__), fname)
            with io.open(filepath, "rt", encoding="utf8") as f:
                return f.read()
        except:
            if not fail_silently:
                raise
            return ""

    @staticmethod
    def requirements(fname):
        """
        Create a list of requirements from the output of the pip freeze command
        saved in a text file.
        """
        packages = Setup.read(fname, fail_silently=True).split("\n")
        packages = (p.strip() for p in packages)
        packages = (p for p in packages if p and not p.startswith("#"))
        packages = (p for p in packages if p and not p.startswith("https://"))
        packages = (p for p in packages if p and not p.startswith("-r "))
        return list(packages)

    @classmethod
    def extra_requirements(cls, glob_pattern):
        before, after = glob_pattern.split("*", 1)
        pattern = os.path.join(os.path.dirname(__file__), glob_pattern)
        requirements = {}
        for path in glob.glob(pattern):
            name = path[len(before) : -len(after)]
            requirements[name] = cls.requirements(path)
        return requirements

    @staticmethod
    def get_files(*bases):
        """
        List all files in a data directory.
        """
        for base in bases:
            basedir, _ = base.split(".", 1)
            base = os.path.join(os.path.dirname(__file__), *base.split("."))

            rem = len(os.path.dirname(base)) + len(basedir) + 2

            for root, dirs, files in os.walk(base):
                for name in files:
                    yield os.path.join(basedir, root, name)[rem:]

    @staticmethod
    def get_metavar(name):
        data = Setup.read(os.path.join(PACKAGE, "__init__.py"))
        value = (
            re.search(u"__{}__\s*=\s*u?'([^']+)'".format(name), data).group(1).strip()
        )
        return value

    @classmethod
    def version(cls):
        return cls.get_metavar("version")

    @classmethod
    def url(cls):
        return cls.get_metavar("url")

    @classmethod
    def author(cls):
        return cls.get_metavar("author")

    @classmethod
    def email(cls):
        return cls.get_metavar("email")

    @classmethod
    def license(cls):
        return cls.get_metavar("license")

    @staticmethod
    def longdesc():
        return Setup.read("README.rst")

    @staticmethod
    def test_links():
        # Test if hardlinks work. This is a workaround until
        # http://bugs.python.org/issue8876 is solved
        if hasattr(os, "link"):
            tempfile = __file__ + ".tmp"
            try:
                os.link(__file__, tempfile)
            except OSError as e:
                if e.errno == 1:  # Operation not permitted
                    del os.link
                else:
                    raise
            finally:
                if os.path.exists(tempfile):
                    os.remove(tempfile)


Setup.test_links()

setup(
    name=PACKAGE_NAME,
    version=Setup.version(),
    author=Setup.author(),
    author_email=Setup.email(),
    include_package_data=True,
    zip_safe=False,
    url=Setup.url(),
    license=Setup.license(),
    packages=find_packages(),
    package_dir={PACKAGE: PACKAGE},
    description=DESCRIPTION,
    install_requires=Setup.requirements("requirements.txt"),
    extras_require=Setup.extra_requirements("requirements-*.txt"),
    long_description=Setup.longdesc(),
    entry_points=Setup.read("entry-points.ini", True),
    classifiers=CLASSIFIERS,
)
