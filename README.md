# FastAPI-GRPC Microservices Architecture

## Overview

This project is a microservices-based architecture that integrates multiple technologies, including Django, FastAPI, gRPC, PostgreSQL, RabbitMQ, and the ELK stack. It is designed for scalability, efficient inter-service communication, and robust monitoring.

## Services

### 🛠 Django Service
- **Description**: Handles user authentication and core application logic.
- **Port**: `8000`
- **Dockerfile**: `./django_service/Dockerfile`

### ⚡ FastAPI Service
- **Description**: Provides a lightweight API for book-related operations.
- **Port**: `8100`
- **Dockerfile**: `./fastapi_service/Dockerfile`

### 🔗 gRPC Service
- **Description**: Offers a gRPC interface for efficient microservice communication.
- **Port**: `50051`
- **Dockerfile**: `./grpc_service/Dockerfile`

### 🗄️ PostgreSQL Database
- **Description**: Relational database for storing application data.
- **Port**: `5432`
- **Environment Variables**:
  ```env
  POSTGRES_DB=test_task_database
  POSTGRES_USER=test_task
  POSTGRES_PASSWORD=Lovell32bd
  ```

### 📩 RabbitMQ
- **Description**: Message broker for asynchronous communication between services.
- **Port**: `5672` (default)
- **Management UI**: `http://localhost:15672`

### 📊 ELK Stack (Logging & Monitoring)
- **Components**:
  - **Elasticsearch** (stores logs)
  - **Logstash** (processes and forwards logs)
  - **Kibana** (visualizes logs)
- **Kibana UI**: `http://localhost:5601`

## 🚀 Getting Started

### Prerequisites
Ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🔧 Running the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/deadlovelll/FastAPI-GRPC.git
   cd FastAPI-GRPC
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the services:
   - **Django**: [http://localhost:8000](http://localhost:8000)
   - **FastAPI**: [http://localhost:8100](http://localhost:8100)
   - **RabbitMQ**: [http://localhost:15672](http://localhost:15672)
   - **Kibana**: [http://localhost:5601](http://localhost:5601)

4. Run the tests and get the current coverage
    ```bash
    bash sh_scripts/run_tests.sh
    ```

## 📜 License
This project is licensed under the MIT License.

---

### 📬 Questions?
Feel free to open an issue or reach out via GitHub!