import sys
import subprocess
import os
import tarfile
from setuptools import find_namespace_packages

from pathlib import Path
import pytest


from ansys.tools import protos_generator as pg
from ansys.tools.protos_generator import generator

# ensure we can import the sample directory
HERE = os.path.abspath(os.path.dirname(__file__))
SAMPLE_DIRECTORY = os.path.join(HERE, '..', 'proto-samples', 'ansys',
                                'api', 'sample', 'v1')
if not os.path.isdir(SAMPLE_DIRECTORY):
    raise FileNotFoundError('Unable to locate example protofile directory')


def test_construct_package_name():
    name, package_name, paths = generator.construct_package_name('proto-samples/ansys/api/sample/v1')
    assert name == 'ansys-api-sample-v1'
    assert package_name == 'ansys.api.sample.v1'
    assert paths == ['ansys', 'api', 'sample', 'v1']

    with pytest.raises(ValueError, match='missing the required "ansys"'):
        generator.construct_package_name('api/sample/v1')

    with pytest.raises(ValueError, match='Top level should be a version'):
        generator.construct_package_name('ansys/api/sample/vN')

    with pytest.raises(ValueError, match='Expected a directory structure containing'):
        generator.construct_package_name('ansys/api/sample')

    with pytest.raises(ValueError, match='Expected a directory structure containing'):
        generator.construct_package_name('proto-samples/ansys/api/sample')


def test_parse_version():
    assert generator.parse_version('0.2.0') == (0, 2, 0)

    with pytest.raises(ValueError, match='Invalid version string'):
        generator.parse_version('0.foo.0')


def test_generate(tmpdir):
    output_directory = str(tmpdir.mkdir("tmpdir"))
    dist_file = generator.package_protos(SAMPLE_DIRECTORY, output_directory)
    name, package_name, paths = generator.construct_package_name('proto-samples/ansys/api/sample/v1')

    # verify file is within the output directory
    assert os.path.isfile(os.path.join(output_directory, Path(dist_file).name))

    # verify name in sdist
    assert name in Path(dist_file).name
    assert dist_file.endswith('tar.gz')

    # test import from the tar package
    import tarfile
    tar_directory = str(tmpdir.mkdir("tardir"))
    with tarfile.open(dist_file) as f:
        f.extractall(tar_directory)

    old_dir = os.getcwd()
    pth = Path(dist_file).name.split('.tar.gz')[0]
    os.chdir(os.path.join(tar_directory, pth))

    # verify we can import the module
    packages = find_namespace_packages(include='ansys*')
    assert package_name in packages

    # validate installation
    p = subprocess.Popen(f"{sys.executable} -m pip install {dist_file}",
                         stdout=subprocess.PIPE,
                         shell=True)
    output = p.stdout.read().decode()

    assert f'Successfully installed {name}' in output 

    from ansys.api.sample.v1 import sample_pb2
    assert hasattr(sample_pb2, 'SampleReply')
    assert hasattr(sample_pb2, 'SampleRequest')

    p = subprocess.Popen(f"{sys.executable} -m pip uninstall {name} -y",
                         stdout=subprocess.PIPE,
                         shell=True)
    output = p.stdout.read().decode()
    assert f'Successfully uninstalled {name}' in output


def test_generate_wheel(tmpdir):
    name, package_name, paths = generator.construct_package_name('proto-samples/ansys/api/sample/v1')
    output_directory = str(tmpdir.mkdir("tmpdir"))
    # check wheel works
    whl_file = generator.package_protos(SAMPLE_DIRECTORY, output_directory, wheel=True)
    assert whl_file.endswith('whl')
    assert name.replace('-', '_') in Path(whl_file).name


def test_run_main(tmpdir):
    this_package = 'ansys-tools-protos-generator'
    protopath = 'proto-samples/ansys/api/sample/v1'
    output_directory = str(tmpdir.mkdir("tmpdir"))

    cmd = f"{sys.executable} -m pip {this_package} {protopath} {output_directory}"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
