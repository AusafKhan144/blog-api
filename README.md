# 📝 Blog API (FastAPI)

A simple, containerized RESTful API for a personal blogging platform built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## 📌 Features

- Full CRUD operations for blog articles
- PostgreSQL database integration
- Alembic migrations for schema changes
- Token validation (via dependencies)
- Auto-generated Swagger docs

## 🧱 Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL

## 📦 Project Structure

```
└── blog-api
    └── app
        └── __init__.py
        └── config.py
        └── db.py
        └── dependencies.py
        └── endpoints
            └── __init__.py
            └── article.py
        └── main.py
        └── models
            └── __init__.py
            └── article.py
        └── schemas
            └── __init__.py
            └── article.py
    └── migrations
        └── env.py
        └── README
        └── script.py.mako
        └── versions
    └── .env.example
    └── .gitignore
    └── alembic.ini
    └── README.md
    └── Dockerfile
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AusafKhan144/blog-api.git
cd blog-api
```

### 3. Environment Configuration

This project uses environment variables for configuration. Create a `.env` file in the project root based on the provided `.env.example` template.

#### 📄 `.env.example`

```env
DATABASE_USER=your_db_username
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=your_db_name
SERVICE_KEY=your_service_secret_key
```
> ℹ️ The `SERVICE_KEY` can be used for securing routes or internal service authentication.  
> The `DATABASE_HOST` should match your database container name if using Docker (e.g., `db`).

Once you've updated the `.env.example` file with your credentials, rename it to `.env` to enable the app to load the configuration.

> **Note:** Make sure not to commit your `.env` file to version control as it contains sensitive data. The `.env.example` file is safe for sharing and version control.


### 3. Running with Docker

   ```bash
   docker build -t blog-api .
   docker run -d -p 8000:8000 --env-file .env blog-api
   ```
   

## 📖 API Documentation

You can explore the API using the built-in interactive docs:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
