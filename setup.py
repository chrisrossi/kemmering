import os, sys
from setuptools import setup
from setuptools import find_packages

VERSION = '1.0.3'

requires = []
tests_require = requires + ['pytest']
testing_extras = tests_require + ['pytest-cov', 'tox', 'flake8']
docs_extras = ['Sphinx', 'pylons-sphinx-themes >= 0.3']

here = os.path.abspath(os.path.dirname(__file__))
if sys.version_info[0] > 2:
    README = open(os.path.join(here, 'README.rst'), encoding="utf-8").read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt'), encoding="utf-8").read()
else:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()


setup(
    name='kemmering',
    version=VERSION,
    description='Super simple XMLish tags',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: XML",
        "License :: Repoze Public License",
    ],
    keywords='web html pylons xml templates',
    author='Chris Rossi',
    author_email='pylons-discuss@googlegroups.com',
    maintainer='Chris Rossi',
    maintainer_email='pylons-discuss@googlegroups.com',
    url='https://github.com/chrisrossi/kemmering',
    license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'testing': testing_extras,
        'docs': docs_extras,
    }
)
