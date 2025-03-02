
# Library Management System

## Concept

The **Library Management System** is a distributed application designed to manage library operations efficiently. It consists of two independent services:

- **Admin API**: Used by library administrators to manage books and monitor user activity.
- **Frontend API**: Used by library members to browse books, enroll in the library, and borrow books.

The two services communicate asynchronously using **Apache Kafka**, ensuring data consistency across the system while maintaining loose coupling between services.


## Features

### Admin API Features

- **Add/Remove Books**: Add new books to the library or remove outdated ones.
- **List Books**: View all books in the library.
- **View Users**: See all enrolled library members.
- **Monitor Borrows**: Track which books are borrowed and their due dates.

### Frontend API Features

- **Enroll Users**: Allow new members to join the library.
- **Browse Books**: View available books with filtering options (by publisher/category).
- **Borrow Books**: Members can borrow books for a specified number of days.
- **Book Availability**: Real-time updates on book availability.

## How It Works

1. **Admin adds a book** → Book is synced to Frontend via Kafka.
2. **User enrolls** → User data is synced to Admin via Kafka.
3. **User borrows a book** → Borrow record is synced to Admin via Kafka.
4. **Book availability** is updated in real-time across both services.



## Getting Started

### Prerequisites

- **Docker**
- **Docker Compose**

### Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/library-management.git
  cd library-management
  ```

2. Start the services:
  ```bash
  docker-compose up --build
  ```
  This will start:
  - Admin API at http://localhost:8000/admin/
  - Frontend API at http://localhost:8001/api/
  - Kafka for message brokering
  - MySQL databases for each service

3. Verify Services
  Check if all services are running:
  ```bash
  docker-compose ps
  ```
  You should see:
  - library-management-admin-api-1
  - library-management-frontend-api-1
  - library-management-kafka-1
  - library-management-zookeeper-1
  - library-management-admin-db-1
  - library-management-frontend-db-1

### Testing the Application

1. Enroll a User (Frontend API)
  Send a POST request to http://localhost:8001/api/enroll/ with the following payload:
  ```json
  {
    "email": "user@example.com",
    "firstname": "John",
    "lastname": "Doe"
  }
  ```

2. Add a Book (Admin API)
  Send a POST request to http://localhost:8000/admin/books/ with the following payload:
  ```json
  {
    "title": "Atomic Habits",
    "publisher": "James Clear",
    "category": "Self Help"
  }
  ```

3. Borrow a Book (Frontend API)
  Send a POST request to http://localhost:8001/api/borrow/ with the following payload:
  ```json
  {
    "user_email": "user@example.com",
    "book_id": 1,
    "days": 14
  }
  ```

4. View Borrowed Books (Admin API)
  Send a GET request to http://localhost:8000/admin/borrows/ to view all borrowed books.

### Stopping the Application

To stop all services:
  ```bash
  docker-compose down
  ```

To stop and remove all data (including databases):
  ```bash
  docker-compose down -v
  ```

### Troubleshooting

#### Common Issues

- **Kafka not starting**: Ensure Docker has at least 4GB of memory allocated.
- **Database connection errors**: Wait for MySQL to fully initialize (2-3 minutes).
- **Services not syncing**: Check Kafka logs:
  ```bash
  docker-compose logs kafka
  ```



