import os

from concurrent import futures

import grpc
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc
from grpc_service.controllers.book_controller.book_controller import BookService

class GRPCServerFactory:
    
    """
    Factory for creating a gRPC server instance with the BookService.
    
    Attributes:
        max_workers (int): The maximum number of worker threads for the gRPC server.
        port (int): The port on which the gRPC server will listen.
    """

    def __init__ (
        self, 
        max_workers: int = int(os.getenv('GRPC_SERVER_PORT')), 
        port: int = int(os.getenv('GRPC_MAX_WORKERS')),
    ) -> None:
        
        """
        Initialize the GRPCServerFactory with the specified number of workers and port.

        Args:
            max_workers (int): Maximum number of threads in the thread pool.
            port (int): Port number for the gRPC server.
        """
        
        self.max_workers = max_workers
        self.port = port

    def create_server (
        self,
    ) -> grpc.Server:
        
        """
        Creates and configures the gRPC server with the BookService.

        Returns:
            grpc.Server: A fully configured gRPC server instance.
        """
        
        book_service = BookService()
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        books_pb2_grpc.add_BookServiceServicer_to_server(book_service, server)
        server.add_insecure_port(f'[::]:{self.port}')
        return server


def serve() -> None:
    
    """
    Initializes the gRPC server using GRPCServerFactory and starts it.
    
    The server runs indefinitely until terminated.
    """
    
    factory = GRPCServerFactory()
    server = factory.create_server()
    print(f'gRPC server running on port {factory.port}...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
