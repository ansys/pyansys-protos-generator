import argparse
from .generator import package_grpc

DESC = """Create a Python package from autogenerated API files"""

def main():
    """Package auto-generated grpc python client protocols

    Package name will match the grpc package name.

    For example, in a protofile named

    ./ansys/api/sample-examples.v1;

    Expects there to be a VERSION file in the directory containing the
    protocols.

    """
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('grpc_source_path',
                        type=str,
                        help='Path containing gRPC protobuf files')

    args = parser.parse_args()
    package_grpc(args.grpc_source_path)


if __name__ == '__main__':
    main()
