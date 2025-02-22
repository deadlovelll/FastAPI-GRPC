import pika
import grpc
import json

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import grpc_service.grpc_server.grpc_server as grpc_server
import grpc_service.books_pb2_grpc as books_pb2_grpc

import grpc_service.books_pb2 as books_pb2

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)

channel = connection.channel()

channel.queue_declare(queue='book_queue')

def send_message(message):
    channel.basic_publish(exchange='', routing_key='book_queue', body=message)
    print(f"Sent: {message}")

def callback(ch, method, properties, body):
        
        message = body.decode()
        print("Received message:", message)

        parts = message.split('|')
        
        print(parts)
    
        if parts[0]  == 'Posting Book':
            print('posting book request')
            
            with grpc.insecure_channel('localhost:50051') as channel:
                
                stub = books_pb2_grpc.BookServiceStub(channel)
                
                request = books_pb2.PostBookRequest(book_name=parts[1], book_author=parts[2])
                
                response = stub.PostBook(request)
                print('Book created')
                
        elif parts[0] == 'Deleting Book':
            
            print('deleting book request')
            
            with grpc.insecure_channel('localhost:50051') as channel:
                
                stub = books_pb2_grpc.BookServiceStub(channel)
                
                request = books_pb2.DeleteBookRequest(book_id=int(parts[1]))
                
                response = stub.DeleteBook(request)
                print('Book Deleted')
                
        elif parts[0] == 'Editing Book':
            
            print('updating book request')
            
            with grpc.insecure_channel('localhost:50051') as channel:
                
                stub = books_pb2_grpc.BookServiceStub(channel)
                
                request = books_pb2.UpdateBookRequest(book_id=int(parts[1]), book_name=parts[2], author=parts[3])
                
                response = stub.UpdateBook(request)
                print('Book Updated')

channel.basic_consume(queue='book_queue', on_message_callback=callback, auto_ack=True)

if __name__ == '__main__':
    send_message('Hello, RabbitMQ!')

    print('Waiting for messages...')
    channel.start_consuming()
