# Product Review System (PRS) - Backend API

A robust, high-performance RESTful API built with **Django Rest Framework (DRF)**. This project implements a complete product review ecosystem with advanced features like caching, throttling, and a voting system.

## 🚀 Key Features

- **Product & Category Management:** Full CRUD operations with Slug-based lookups.
- **Advanced Review System:** Users can review products once, with real-time average rating calculation.
- **Review Voting:** "Upvote/Downvote" logic for reviews with automatic vote toggling.
- **Favorites System:** Users can manage a personalized list of favorite products.
- **Performance Optimization:** - **Redis Caching:** Drastic reduction in DB queries using `django-redis`.
    - **Pagination:** Structured data delivery for better frontend performance.
- **Security & Protection:**
    - **Custom Permissions:** Object-level permissions (Admin vs Owner).
    - **Throttling:** Protection against Spamming (Custom rates for review creation).
- **Automated Workflows:** Django Signals for automatic cache invalidation and email notifications.

## 🛠️ Tech Stack

* **Framework:** Django & Django Rest Framework (DRF)
* **Database:** PostgreSQL (Production) / SQLite (Development)
* **Caching:** Redis
* **Documentation:** Swagger UI (drf-spectacular)

Manual Setup
Install requirements: pip install -r requirements.txt

Configure your .env file.

Run migrations: python manage.py migrate

Start Redis server locally.

Run server: python manage.py runserver

📖 API Documentation
Once the server is running, you can explore the interactive API documentation:

Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/

Redoc: http://127.0.0.1:8000/api/schema/redoc/