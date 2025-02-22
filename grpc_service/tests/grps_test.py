import unittest
from concurrent import futures
import grpc
import grpc_service.books_pb.books_pb2 as books_pb2
import grpc_service.books_pb.books_pb2_grpc as books_pb2_grpc
import grpc_service.grpc_server.grpc_server as grpc_server

class TestBookService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        cls.book_service = grpc_server.BookService()
        books_pb2_grpc.add_BookServiceServicer_to_server(cls.book_service, cls.server)
        cls.server.add_insecure_port('[::]:50051')
        cls.server.start()

        cls.channel = grpc.insecure_channel('localhost:50051')
        cls.stub = books_pb2_grpc.BookServiceStub(cls.channel)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(0)
        cls.channel.close()

    def test_post_book(self):
        book = books_pb2.BookRequest(book_name="Test Book", book_author="Author Name")
        response = self.stub.PostBook(book)
        self.assertIsNotNone(response)
        self.assertEqual(response.book_name, "Test Book")

    def test_get_book_by_id(self):
        book_id = 1  
        request = books_pb2.GetBookRequest(book_id=book_id)
        response = self.stub.GetBookById(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.id, book_id)

    def test_get_all_books(self):
        request = books_pb2.Empty()  
        response = self.stub.GetAllBooks(request)
        self.assertIsNotNone(response)
        self.assertGreater(len(response.books), 0)

    def test_update_book(self):
        book_id = 1  
        book_update = books_pb2.UpdateBookRequest(book_id=book_id, book_name="Updated Book")
        response = self.stub.UpdateBook(book_update)
        self.assertIsNotNone(response)
        self.assertEqual(response.id, book_id)
        self.assertEqual(response.book_name, "Updated Book")

    def test_delete_book(self):
        book_id = 1  
        request = books_pb2.DeleteBookRequest(book_id=book_id)
        response = self.stub.DeleteBook(request)
        self.assertIsNotNone(response)
        self.assertEqual(response.id, book_id)

if __name__ == '__main__':
    unittest.main()
