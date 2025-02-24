from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder


_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 27, 2, '', 'books.proto'
)

_sym_db = _symbol_database.Default()

from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0b\x62ooks.proto\x12\x04\x62ook\x1a\x1fgoogle/protobuf/timestamp.proto'
    b'\"\x1e\n\x0b\x42ookRequest\x12\x0f\n\x07\x62ook_id\x18\x01 \x01(\x05'
    b'\"\x0e\n\x0c\x45mptyRequest'
    b'\"n\n\x0c\x42ookResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x11\n\tbook_name'
    b'\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t\x12/\n\x0buploaded_at'
    b'\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp'
    b'\"2\n\rBooksResponse\x12!\n\x05\x62ooks\x18\x01 \x03(\x0b\x32\x12.book.BookResponse'
    b'\"9\n\x0fPostBookRequest\x12\x11\n\tbook_name\x18\x01 \x01(\t\x12\x13\n\x0b\x62ook_author'
    b'\x18\x02 \x01(\t'
    b'\"$\n\x11\x44\x65leteBookRequest\x12\x0f\n\x07\x62ook_id\x18\x01 \x01(\x05'
    b'\"G\n\x11UpdateBookRequest\x12\x0f\n\x07\x62ook_id\x18\x01 \x01(\x05'
    b'\x12\x11\n\tbook_name\x18\x02 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x03 \x01(\t'
    b'2\xa8\x02\n\x0b\x42ookService\x12\x34\n\x0bGetBookById\x12\x11.book.BookRequest'
    b'\x1a\x12.book.BookResponse'
    b'\x12\x36\n\x0bGetAllBooks\x12\x12.book.EmptyRequest\x1a\x13.book.BooksResponse'
    b'\x12\x35\n\x08PostBook\x12\x15.book.PostBookRequest\x1a\x12.book.BookResponse'
    b'\x12\x39\n\nDeleteBook\x12\x17.book.DeleteBookRequest\x1a\x12.book.BookResponse'
    b'\x12\x39\n\nUpdateBook\x12\x17.book.UpdateBookRequest\x1a\x12.book.BookResponse'
    b'b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'books_pb2', _globals)

if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_BOOKREQUEST']._serialized_start = 54
    _globals['_BOOKREQUEST']._serialized_end = 84
    _globals['_EMPTYREQUEST']._serialized_start = 86
    _globals['_EMPTYREQUEST']._serialized_end = 100
    _globals['_BOOKRESPONSE']._serialized_start = 102
    _globals['_BOOKRESPONSE']._serialized_end = 212
    _globals['_BOOKSRESPONSE']._serialized_start = 214
    _globals['_BOOKSRESPONSE']._serialized_end = 264
    _globals['_POSTBOOKREQUEST']._serialized_start = 266
    _globals['_POSTBOOKREQUEST']._serialized_end = 323
    _globals['_DELETEBOOKREQUEST']._serialized_start = 325
    _globals['_DELETEBOOKREQUEST']._serialized_end = 361
    _globals['_UPDATEBOOKREQUEST']._serialized_start = 363
    _globals['_UPDATEBOOKREQUEST']._serialized_end = 434
    _globals['_BOOKSERVICE']._serialized_start = 437
    _globals['_BOOKSERVICE']._serialized_end = 733
# @@protoc_insertion_point(module_scope)
