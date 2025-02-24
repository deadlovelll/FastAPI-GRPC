import warnings
from typing import Any, Sequence

import grpc

import grpc_service.books_pb.books_pb2 as books__pb2

GRPC_GENERATED_VERSION = "1.66.1"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        (
            f"The grpc package installed is at version {GRPC_VERSION}, but the generated code in "
            f"books_pb2_grpc.py depends on grpcio>={GRPC_GENERATED_VERSION}. Please upgrade your "
            f"grpc module to grpcio>={GRPC_GENERATED_VERSION} or downgrade your generated code using "
            f"grpcio-tools<={GRPC_VERSION}."
        )
    )


class BookServiceStub:
    
    """
    Stub client for the BookService defined in the protobuf.
    
    This class provides methods to call remote procedures defined in the BookService.
    """

    def __init__ (
        self, 
        channel: grpc.Channel,
    ) -> None:
        
        """
        Constructor.

        Args:
            channel (grpc.Channel): The channel used for RPC communication.
        """
        
        self.GetBookById = channel.unary_unary(
            "/book.BookService/GetBookById",
            request_serializer=books__pb2.BookRequest.SerializeToString,
            response_deserializer=books__pb2.BookResponse.FromString,
            _registered_method=True,
        )
        self.GetAllBooks = channel.unary_unary(
            "/book.BookService/GetAllBooks",
            request_serializer=books__pb2.EmptyRequest.SerializeToString,
            response_deserializer=books__pb2.BooksResponse.FromString,
            _registered_method=True,
        )
        self.PostBook = channel.unary_unary(
            "/book.BookService/PostBook",
            request_serializer=books__pb2.PostBookRequest.SerializeToString,
            response_deserializer=books__pb2.BookResponse.FromString,
            _registered_method=True,
        )
        self.DeleteBook = channel.unary_unary(
            "/book.BookService/DeleteBook",
            request_serializer=books__pb2.DeleteBookRequest.SerializeToString,
            response_deserializer=books__pb2.BookResponse.FromString,
            _registered_method=True,
        )
        self.UpdateBook = channel.unary_unary(
            "/book.BookService/UpdateBook",
            request_serializer=books__pb2.UpdateBookRequest.SerializeToString,
            response_deserializer=books__pb2.BookResponse.FromString,
            _registered_method=True,
        )



import grpc

class BookServiceServicer(object):
    
    """
    Base class for the BookService gRPC service.

    This class provides unimplemented method stubs for each RPC defined in the
    proto file. Service implementers should subclass this and override the
    methods with concrete implementations.
    """

    def GetBookById (
        self, 
        request, 
        context,
    ):
        
        """
        Retrieves a book by its ID.

        Args:
            request: The GetBookById request message.
            context (grpc.ServicerContext): The context for the gRPC call.

        Raises:
            NotImplementedError: Always raised to indicate that the method is not implemented.
        """
        
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllBooks (
        self, 
        request, 
        context,
    ):
        
        """
        Retrieves all books.

        Args:
            request: The GetAllBooks request message.
            context (grpc.ServicerContext): The context for the gRPC call.

        Raises:
            NotImplementedError: Always raised to indicate that the method is not implemented.
        """
        
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PostBook (
        self, 
        request, 
        context,
    ):
        """
        Creates a new book record.

        Args:
            request: The PostBook request message.
            context (grpc.ServicerContext): The context for the gRPC call.

        Raises:
            NotImplementedError: Always raised to indicate that the method is not implemented.
        """
        
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteBook (
        self, 
        request, 
        context,
    ):
        
        """
        Deletes a book record by its ID.

        Args:
            request: The DeleteBook request message.
            context (grpc.ServicerContext): The context for the gRPC call.

        Raises:
            NotImplementedError: Always raised to indicate that the method is not implemented.
        """
        
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateBook (
        self, 
        request, 
        context,
    ):
        
        """
        Updates an existing book record.

        Args:
            request: The UpdateBook request message.
            context (grpc.ServicerContext): The context for the gRPC call.

        Raises:
            NotImplementedError: Always raised to indicate that the method is not implemented.
        """
        
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BookServiceServicer_to_server (
    servicer, 
    server
):
    
    """
    Adds a BookService servicer to the provided gRPC server by registering
    all RPC method handlers.

    Args:
        servicer: An instance of BookServiceServicer (or subclass) implementing
                  the service methods (e.g., GetBookById, GetAllBooks, PostBook,
                  DeleteBook, UpdateBook).
        server: The gRPC server instance to which the service will be added.
    """
    
    rpc_method_handlers = {
        "GetBookById": grpc.unary_unary_rpc_method_handler (
            servicer.GetBookById,
            request_deserializer=books__pb2.BookRequest.FromString,
            response_serializer=books__pb2.BookResponse.SerializeToString,
        ),
        "GetAllBooks": grpc.unary_unary_rpc_method_handler (
            servicer.GetAllBooks,
            request_deserializer=books__pb2.EmptyRequest.FromString,
            response_serializer=books__pb2.BooksResponse.SerializeToString,
        ),
        "PostBook": grpc.unary_unary_rpc_method_handler (
            servicer.PostBook,
            request_deserializer=books__pb2.PostBookRequest.FromString,
            response_serializer=books__pb2.BookResponse.SerializeToString,
        ),
        "DeleteBook": grpc.unary_unary_rpc_method_handler (
            servicer.DeleteBook,
            request_deserializer=books__pb2.DeleteBookRequest.FromString,
            response_serializer=books__pb2.BookResponse.SerializeToString,
        ),
        "UpdateBook": grpc.unary_unary_rpc_method_handler (
            servicer.UpdateBook,
            request_deserializer=books__pb2.UpdateBookRequest.FromString,
            response_serializer=books__pb2.BookResponse.SerializeToString,
        ),
    }
    
    generic_handler = grpc.method_handlers_generic_handler (
        "book.BookService", rpc_method_handlers,
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers (
        "book.BookService", 
        rpc_method_handlers,
    )


# This class is part of an EXPERIMENTAL API.
class BookService(object):
    
    """
    Experimental gRPC client for BookService.

    This class provides static methods for calling remote procedures defined in the
    BookService service in the books.proto file. It uses the grpc.experimental.unary_unary
    API to perform unary RPC calls.
    """

    @staticmethod
    def GetBookById(
        request: Any,
        target: str,
        options: Sequence[Any] = (),
        channel_credentials: Any = None,
        call_credentials: Any = None,
        insecure: bool = False,
        compression: Any = None,
        wait_for_ready: Any = None,
        timeout: Any = None,
        metadata: Any = None,
    ) -> Any:
        
        """
        Calls the GetBookById RPC method.

        Args:
            request: The BookRequest message.
            target (str): The target server address.
            options (Sequence[Any], optional): Additional channel options.
            channel_credentials (optional): Channel credentials.
            call_credentials (optional): Call credentials.
            insecure (bool, optional): If True, use an insecure channel.
            compression (optional): Compression settings.
            wait_for_ready (optional): Whether to wait for the channel to be ready.
            timeout (optional): The RPC timeout.
            metadata (optional): Additional metadata for the RPC.

        Returns:
            The BookResponse message.
        """
        
        return grpc.experimental.unary_unary (
            request,
            target,
            '/book.BookService/GetBookById',
            books__pb2.BookRequest.SerializeToString,
            books__pb2.BookResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def GetAllBooks(
        request: Any,
        target: str,
        options: Sequence[Any] = (),
        channel_credentials: Any = None,
        call_credentials: Any = None,
        insecure: bool = False,
        compression: Any = None,
        wait_for_ready: Any = None,
        timeout: Any = None,
        metadata: Any = None,
    ) -> Any:
        
        """
        Calls the GetAllBooks RPC method.

        Args:
            request: The EmptyRequest message.
            target (str): The target server address.
            options (Sequence[Any], optional): Additional channel options.
            channel_credentials (optional): Channel credentials.
            call_credentials (optional): Call credentials.
            insecure (bool, optional): If True, use an insecure channel.
            compression (optional): Compression settings.
            wait_for_ready (optional): Whether to wait for the channel to be ready.
            timeout (optional): The RPC timeout.
            metadata (optional): Additional metadata for the RPC.

        Returns:
            The BooksResponse message.
        """
        
        return grpc.experimental.unary_unary(
            request,
            target,
            '/book.BookService/GetAllBooks',
            books__pb2.EmptyRequest.SerializeToString,
            books__pb2.BooksResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def PostBook(
        request: Any,
        target: str,
        options: Sequence[Any] = (),
        channel_credentials: Any = None,
        call_credentials: Any = None,
        insecure: bool = False,
        compression: Any = None,
        wait_for_ready: Any = None,
        timeout: Any = None,
        metadata: Any = None,
    ) -> Any:
        
        """
        Calls the PostBook RPC method.

        Args:
            request: The PostBookRequest message.
            target (str): The target server address.
            options (Sequence[Any], optional): Additional channel options.
            channel_credentials (optional): Channel credentials.
            call_credentials (optional): Call credentials.
            insecure (bool, optional): If True, use an insecure channel.
            compression (optional): Compression settings.
            wait_for_ready (optional): Whether to wait for the channel to be ready.
            timeout (optional): The RPC timeout.
            metadata (optional): Additional metadata for the RPC.

        Returns:
            The BookResponse message.
        """
        
        return grpc.experimental.unary_unary (
            request,
            target,
            '/book.BookService/PostBook',
            books__pb2.PostBookRequest.SerializeToString,
            books__pb2.BookResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def DeleteBook(
        request: Any,
        target: str,
        options: Sequence[Any] = (),
        channel_credentials: Any = None,
        call_credentials: Any = None,
        insecure: bool = False,
        compression: Any = None,
        wait_for_ready: Any = None,
        timeout: Any = None,
        metadata: Any = None,
    ) -> Any:
        
        """
        Calls the DeleteBook RPC method.

        Args:
            request: The DeleteBookRequest message.
            target (str): The target server address.
            options (Sequence[Any], optional): Additional channel options.
            channel_credentials (optional): Channel credentials.
            call_credentials (optional): Call credentials.
            insecure (bool, optional): If True, use an insecure channel.
            compression (optional): Compression settings.
            wait_for_ready (optional): Whether to wait for the channel to be ready.
            timeout (optional): The RPC timeout.
            metadata (optional): Additional metadata for the RPC.

        Returns:
            The BookResponse message.
        """
        
        return grpc.experimental.unary_unary (
            request,
            target,
            '/book.BookService/DeleteBook',
            books__pb2.DeleteBookRequest.SerializeToString,
            books__pb2.BookResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )

    @staticmethod
    def UpdateBook(
        request: Any,
        target: str,
        options: Sequence[Any] = (),
        channel_credentials: Any = None,
        call_credentials: Any = None,
        insecure: bool = False,
        compression: Any = None,
        wait_for_ready: Any = None,
        timeout: Any = None,
        metadata: Any = None,
    ) -> Any:
        
        """
        Calls the UpdateBook RPC method.

        Args:
            request: The UpdateBookRequest message.
            target (str): The target server address.
            options (Sequence[Any], optional): Additional channel options.
            channel_credentials (optional): Channel credentials.
            call_credentials (optional): Call credentials.
            insecure (bool, optional): If True, use an insecure channel.
            compression (optional): Compression settings.
            wait_for_ready (optional): Whether to wait for the channel to be ready.
            timeout (optional): The RPC timeout.
            metadata (optional): Additional metadata for the RPC.

        Returns:
            The BookResponse message.
        """
        
        return grpc.experimental.unary_unary (
            request,
            target,
            '/book.BookService/UpdateBook',
            books__pb2.UpdateBookRequest.SerializeToString,
            books__pb2.BookResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )
