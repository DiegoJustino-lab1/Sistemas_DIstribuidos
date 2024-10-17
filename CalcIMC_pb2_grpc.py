# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import CalcIMC_pb2 as CalcIMC__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in CalcIMC_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class IMCServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CalculoIMC = channel.unary_unary(
                '/IMCService/CalculoIMC',
                request_serializer=CalcIMC__pb2.CalculoIMCRequest.SerializeToString,
                response_deserializer=CalcIMC__pb2.CalculoIMCResponse.FromString,
                _registered_method=True)


class IMCServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CalculoIMC(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IMCServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CalculoIMC': grpc.unary_unary_rpc_method_handler(
                    servicer.CalculoIMC,
                    request_deserializer=CalcIMC__pb2.CalculoIMCRequest.FromString,
                    response_serializer=CalcIMC__pb2.CalculoIMCResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'IMCService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('IMCService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class IMCService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CalculoIMC(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/IMCService/CalculoIMC',
            CalcIMC__pb2.CalculoIMCRequest.SerializeToString,
            CalcIMC__pb2.CalculoIMCResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
