# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/discovery.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15proto/discovery.proto\x12\x05proto\";\n\x15\x44iscoveryLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"&\n\x13\x44iscoveryLoginReply\x12\x0f\n\x07\x63orrect\x18\x01 \x01(\x08\"&\n\x16\x44iscoverySearchRequest\x12\x0c\n\x04\x63ity\x18\x01 \x01(\t\"p\n\x14\x44iscoverySearchReply\x12\x0f\n\x07\x63orrect\x18\x01 \x01(\x08\x12\x0c\n\x04\x63ity\x18\x02 \x01(\t\x12\x13\n\x0btemperature\x18\x03 \x01(\x02\x12\x10\n\x08humidity\x18\x04 \x01(\x02\x12\x12\n\ncloudiness\x18\x05 \x01(\t\"/\n\nPutRequest\x12\x13\n\x0bserviceName\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\t\"\x1a\n\x08PutReply\x12\x0e\n\x06result\x18\x01 \x01(\x08\x32\xd8\x01\n\x10\x44iscoveryService\x12J\n\x0e\x64iscoveryLogin\x12\x1c.proto.DiscoveryLoginRequest\x1a\x1a.proto.DiscoveryLoginReply\x12M\n\x0f\x64iscoverySearch\x12\x1d.proto.DiscoverySearchRequest\x1a\x1b.proto.DiscoverySearchReply\x12)\n\x03put\x12\x11.proto.PutRequest\x1a\x0f.proto.PutReplyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.discovery_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DISCOVERYLOGINREQUEST']._serialized_start=32
  _globals['_DISCOVERYLOGINREQUEST']._serialized_end=91
  _globals['_DISCOVERYLOGINREPLY']._serialized_start=93
  _globals['_DISCOVERYLOGINREPLY']._serialized_end=131
  _globals['_DISCOVERYSEARCHREQUEST']._serialized_start=133
  _globals['_DISCOVERYSEARCHREQUEST']._serialized_end=171
  _globals['_DISCOVERYSEARCHREPLY']._serialized_start=173
  _globals['_DISCOVERYSEARCHREPLY']._serialized_end=285
  _globals['_PUTREQUEST']._serialized_start=287
  _globals['_PUTREQUEST']._serialized_end=334
  _globals['_PUTREPLY']._serialized_start=336
  _globals['_PUTREPLY']._serialized_end=362
  _globals['_DISCOVERYSERVICE']._serialized_start=365
  _globals['_DISCOVERYSERVICE']._serialized_end=581
# @@protoc_insertion_point(module_scope)
