import os
import unittest
from concurrent import futures
from unittest.mock import patch

import grpc

import grpc_service.books_pb.books_pb2 as books_pb2
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc
from grpc_service.grpc_server.grpc_server import GRPCServerFactory

class TestGRPCServer(unittest.TestCase):
    
    """
    Unit tests for verifying the functionality of the gRPC server.
    
    Uses `unittest` for test case management and `patch.dict` to override environment variables.
    """
    
    @patch.dict (
        os.environ, 
        {
            "GRPC_SERVER_PORT": "50051", 
            "GRPC_MAX_WORKERS": "10"
        }
    )
    def setUp (
        self,
    ) -> None:
        
        """
        Sets up the test environment before execution.

        - Creates an instance of `GRPCServerFactory`
        - Starts the gRPC server in a separate thread
        - Establishes a connection with the server using `grpc.insecure_channel`
        """
        
        self.factory = GRPCServerFactory()
        self.server = self.factory.create_server()
        
        self.server_thread = futures.ThreadPoolExecutor(max_workers=1)
        self.server_thread.submit(self.server.start)

        self.channel = grpc.insecure_channel(f'localhost:{self.factory.port}')
        self.stub = books_pb2_grpc.BookServiceStub(self.channel)

    def test_grpc_server_is_running (
        self,
    ) -> None:
        
        """
        Tests whether the gRPC server is running and responding.

        Sends a `GetAllBooks` request and verifies that a response is received.
        """
        
        try:
            response = self.stub.GetAllBooks(books_pb2.EmptyRequest())
            self.assertIsNotNone(response)
            
        except grpc.RpcError as e:
            self.fail(f"gRPC сервер не отвечает: {e}")

    def tearDown (
        self,
    ) -> None:
        
        """
        Cleans up resources after each test.

        - Stops the gRPC server
        - Shuts down the thread executor
        """
        
        self.server.stop(0)
        self.server_thread.shutdown(wait=True)


if __name__ == "__main__":
    unittest.main()
