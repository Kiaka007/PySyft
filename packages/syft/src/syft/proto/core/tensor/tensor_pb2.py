# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/tensor/tensor.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.adp import entity_pb2 as proto_dot_core_dot_adp_dot_entity__pb2
from syft.proto.lib.numpy import array_pb2 as proto_dot_lib_dot_numpy_dot_array__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1eproto/core/tensor/tensor.proto\x12\x10syft.core.tensor\x1a\x1bproto/core/adp/entity.proto\x1a\x1bproto/lib/numpy/array.proto"\xd4\x01\n\x06Tensor\x12\x10\n\x08obj_type\x18\x02 \x01(\t\x12*\n\x06\x65ntity\x18\x03 \x01(\x0b\x32\x15.syft.core.adp.EntityH\x00\x88\x01\x01\x12\x13\n\x0buse_tensors\x18\x04 \x01(\x08\x12*\n\x06\x61rrays\x18\x05 \x03(\x0b\x32\x1a.syft.lib.numpy.NumpyProto\x12)\n\x07tensors\x18\x06 \x03(\x0b\x32\x18.syft.core.tensor.Tensor\x12\x15\n\rrequires_grad\x18\x07 \x01(\x08\x42\t\n\x07_entityb\x06proto3'
)

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR, "proto.core.tensor.tensor_pb2", globals()
)
if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _TENSOR._serialized_start = 111
    _TENSOR._serialized_end = 323
# @@protoc_insertion_point(module_scope)
