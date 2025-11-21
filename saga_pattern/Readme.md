# Saga Pattern Implementation

This project demonstrates the implementation of the Saga pattern for managing distributed transactions in a microservices architecture. The Saga pattern ensures data consistency across multiple services by coordinating a sequence of local transactions.

## Architecture Overview

The project consists of two main microservices:

- **Order Service**: Handles order creation and management
- **Customer Service**: Manages customer data and payment processing

Communication between services is handled through RabbitMQ message broker using an event-driven approach.

## Tech Stack

### Backend

- **Python 3.11**
- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation using Python type annotations
- **aio-pika** - Asynchronous RabbitMQ client

### Databases

- **PostgreSQL** - Primary database for both services
- **RabbitMQ** - Message broker for inter-service communication

### Infrastructure

- **Docker & Docker Compose** - Containerization and orchestration
- **Docker Networks** - Service isolation and communication

## Project Structure

```
saga_pattern/
├── docker-compose.yml          # Container orchestration
├── order/                      # Order microservice
│   ├── src/
│   │   ├── controller/         # API endpoints
│   │   ├── config.py          # Configuration settings
│   │   ├── database.py        # Database connection
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── schema.py          # Pydantic schemas
│   │   ├── services.py        # Business logic
│   │   ├── rabbitmq.py        # Message broker client
│   │   ├── message_handlers.py # Event handlers
│   │   └── main.py            # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── customer/                   # Customer microservice
│   ├── src/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schema.py
│   │   ├── domain.py          # Domain logic
│   │   ├── rabbitmq.py
│   │   ├── message_handlers.py
│   │   └── initialize_data.py
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

## Saga Flow

1. **Order Creation**: Client creates an order through Order Service
2. **Event Publishing**: Order Service publishes `order.created` event
3. **Payment Processing**: Customer Service receives the event and processes payment
4. **Balance Check**: Customer Service verifies customer balance
5. **Response**: Customer Service publishes either `order.fulfilled` or `order.rejected` event
6. **Order Update**: Order Service receives the response and updates order status

## Services

### Order Service

- **Port**: 8001
- **Database**: PostgreSQL (port 5431)
- **Endpoints**:
  - `POST /orders/` - Create new order
  - `GET /` - Health check

### Customer Service

- **Port**: 8002
- **Database**: PostgreSQL (port 5433)
- **Functions**:
  - Customer balance verification
  - Payment processing
  - Order fulfillment/rejection

### Infrastructure Services

- **RabbitMQ**: Port 5671 (AMQP), 15672 (Management UI)
- **Databases**: PostgreSQL instances for each service

## How to Run

### Prerequisites

- Docker
- Docker Compose

### Quick Start

1. **Clone the repository**

   ```bash
   cd saga_pattern
   ```

2. **Start all services**

   ```bash
   docker-compose up -d
   ```

3. **Check service status**

   ```bash
   docker-compose ps
   ```

4. **View logs**

   ```bash
   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f order-service
   ```

### Testing the Saga

1. **Access Order Service**

   ```bash
   curl http://localhost:8001/
   ```

2. **Create an order**

   ```bash
   curl -X POST "http://localhost:8001/orders/" \
        -H "Content-Type: application/json" \
        -d '{
          "customer_id": 1,
          "product_id": 1,
          "status": "pending",
          "quantity": 1,
          "total_price": 50.0
        }'
   ```

3. **Monitor RabbitMQ**
   - Open http://localhost:15672
   - Login: guest/guest
   - Check exchanges and queues

### Stopping Services

```bash
docker-compose down

# Remove volumes (data will be lost)
docker-compose down -v
```

## Environment Variables

Each service uses environment variables for configuration:

### Order Service

- `DATABASE_URL` - PostgreSQL connection string
- `RABBITMQ_BROKER_URL` - RabbitMQ connection URL

### Customer Service

- `DATABASE_URL` - PostgreSQL connection string
- `RABBITMQ_BROKER_URL` - RabbitMQ connection URL

## Development

### Adding New Services

1. Create service directory with Dockerfile
2. Add service to `docker-compose.yml`
3. Implement message handlers for saga coordination
4. Update network configuration

### Monitoring

- RabbitMQ Management UI: http://localhost:15672
- Service logs: `docker-compose logs -f [service-name]`

## Benefits of This Implementation

- **Eventual Consistency**: Ensures data consistency across services
- **Fault Tolerance**: Handles partial failures gracefully
- **Scalability**: Services can scale independently
- **Decoupling**: Services communicate through events, not direct calls
- **Observability**: Clear event flow for monitoring and debugging
