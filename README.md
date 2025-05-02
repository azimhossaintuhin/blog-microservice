# 📝 Blog Microservice

A microservices-based blog platform built using FastAPI, Tortoise ORM, MySQL, and Docker. The system is divided into independent services for users, posts, and comments—each service operates separately to enhance modularity and maintainability.

---

## 📦 Features

- 🧍‍♂️ **User Service**: Register and manage user accounts
- ✍️ **Post Service**: Create, read, update, and delete blog posts
- 💬 **Comment Service**: Add and view comments on posts
- 🐳 **Dockerized**: Each service runs in its own container
- 📚 **Swagger UI**: Interactive API documentation available per service

---

## 🧱 Architecture

Each microservice is a standalone FastAPI app with its own database connection. There is **no centralized API gateway**; clients must access each service individually.

```
blog-microservice/
├── apps/
│   ├── post_service/        # Handles blog post operations
│   ├── user_service/        # Handles user-related actions
│   └── comment_service/     # Handles comment functionalities
├── mysql-init/
│   └── init.sql             # Initializes MySQL schema
├── docker-compose.yml       # Defines all services and DB in Docker
└── README.md
```

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **ORM**: Tortoise ORM
- **Database**: MySQL
- **Language**: Python 3.10+
- **Containerization**: Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/azimhossaintuhin/blog-microservice.git
   cd blog-microservice
   ```

2. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

3. Access each service using its port:
   - User Service: `http://localhost:<user_port>/docs`
   - Post Service: `http://localhost:<post_port>/docs`
   - Comment Service: `http://localhost:<comment_port>/docs`

   Replace `<user_port>`, `<post_port>`, and `<comment_port>` with the actual ports defined in `docker-compose.yml`.

---

## ✅ Testing

Navigate into any service directory and run:

```bash
pytest
```

(Ensure dependencies are installed if testing outside of Docker.)

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Azim Hossain Tuhin**  
GitHub: [@azimhossaintuhin](https://github.com/azimhossaintuhin)
