"""Ansys protos generator packaging tool."""
import codecs
import os
from io import open as io_open

from setuptools import setup

# loosely from https://packaging.python.org/guides/single-sourcing-package-version/
HERE = os.path.abspath(os.path.dirname(__file__))

__version__ = None
version_file = os.path.join(HERE, 'ansys', 'tools', 'protos_generator', '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())


def read(rel_path):
    with codecs.open(os.path.join(HERE, rel_path), 'r') as fp:
        return fp.read()


# Get the long description from the README file
with open(os.path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ansys-tools-protos-generator',
    packages=['ansys.tools.protos_generator'],
    version=__version__,
    description='PyAnsys Protos Generator Packaging Tool',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/pyansys/pyansys-protos-generator/',
    license='MIT',
    author='ANSYS, Inc.',
    maintainer='Alexander Kaszynski',
    maintainer_email='alexander.kaszynski@ansys.com',
    install_requires=['grpcio-tools', 'wheel', 'twine'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
