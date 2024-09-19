# Project Title

## Overview

This project is a microservices architecture that includes Django, FastAPI, gRPC, PostgreSQL, RabbitMQ, and ELK stack for logging and monitoring. The services communicate with each other and provide a robust environment for building scalable applications.

## Services

### Django Service

- **Description**: This service handles user authentication and the main application logic.
- **Port**: 8000
- **Dockerfile**: `./django_service/Dockerfile`

### FastAPI Service

- **Description**: This service provides a lightweight API for handling book-related operations.
- **Port**: 8100
- **Dockerfile**: `./fastapi_service/Dockerfile`

### gRPC Service

- **Description**: This service provides a gRPC interface for efficient communication between microservices.
- **Port**: 50051
- **Dockerfile**: `./grpc_service/Dockerfile`

### PostgreSQL Database

- **Description**: The relational database used for storing application data.
- **Port**: 5432
- **Environment Variables**:
  - `POSTGRES_DB`: test_task_database
  - `POSTGRES_USER`: test_task
  - `POSTGRES_PASSWORD`: Lovell32bd

### RabbitMQ

- **Description**: Message broker for handling asynchronous communication between services.
- **Port**: 5672 (default)

### ELK Stack

- **Description**: Stack for logging and monitoring application events.
- **Components**: Elasticsearch, Logstash, Kibana

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-project-directory>

2. Start the services:

  docker-compose up --build

3. Access the services:

Django: http://localhost:8000
FastAPI: http://localhost:8100
RabbitMQ: http://localhost:15672 (default user: guest, password: guest)
Kibana: http://localhost:5601

