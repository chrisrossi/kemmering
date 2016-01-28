from setuptools import setup
from setuptools import find_packages

VERSION = '0.1dev'

requires = [
]
tests_require = requires + ['pytest']
testing_extras = tests_require + ['pytest-cov']

setup(
    name='kemmering',
    version=VERSION,
    description='Super simple XML tags',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'testing': testing_extras,
    }
)
