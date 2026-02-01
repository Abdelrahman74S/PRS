# Product Review System (PRS)

A powerful Backend API built with Django and Django REST Framework (DRF) designed to manage products, user reviews, and personalized favorites. The system includes advanced features like request throttling, custom permissions, and automated profile management.

## Key Features

- **Product Management**: Full CRUD operations for products including name, description, and pricing
- **Advanced Review System**: Allows users to post ratings and text reviews for products
- **Favorites List**: Users can bookmark products to a personal "Favorite" list
- **Security & Throttling**:
  - **Custom Permissions**: Ensures only owners can edit or delete their reviews and profiles
  - **Rate Limiting**: Custom throttling (e.g., `ReviewRateThrottle`) to prevent spam and API abuse
- **Search & Filtering**: Integrated `django-filter` to search products by specific criteria
- **Automated Profiles**: Uses Django Signals to automatically create a `UserProfile` whenever a new `User` is registered

## Tech Stack

- **Backend**: Django 5.x
- **API Framework**: Django REST Framework
- **Database**: SQLite (Default)
- **Filtering**: django-filter
- **Authentication**: Token-based/Session-based via DRF

## Getting Started

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Abdelrahman74S/PRS.git
   cd prs
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints Summary

### Accounts

- `POST /accounts/register/` - Create a new user account
- `GET /accounts/profile/` - View or update the authenticated user's profile

### Reviews & Products

- `GET /review/products/` - List all products with filtering options
- `POST /review/products/` - Add a new product (Admin/Owner)
- `GET /review/reviews/` - List all product reviews
- `POST /review/reviews/` - Submit a new review for a product
- `GET /review/favorites/` - View your list of favorite products

## Project Structure Highlights

- **`Review/models.py`**: Defines the core logic for `Product`, `Review`, and `FavoriteProduct`
- **`Review/signals.py`**: Handles the automatic creation of user profiles
- **`Review/throttling.py`**: Contains custom rate-limiting logic for the API
- **`Review/permission.py`**: Custom logic to verify object ownership before modification

## Features in Detail

### Custom Permissions

The system implements custom permission classes to ensure:
- Users can only edit or delete their own reviews
- Profile modifications are restricted to the profile owner
- Product management is restricted to authorized users

### Rate Limiting

Custom throttling classes prevent API abuse:
- `ReviewRateThrottle`: Limits the number of review submissions per user
- Configurable rate limits to balance user experience and system protection

### Automated Profile Creation

Django signals automatically create user profiles:
- When a new user registers, a corresponding `UserProfile` is created
- Ensures data consistency without manual intervention

## Contact
For questions or feedback, please open an issue on the [GitHub repository](https://github.com/Abdelrahman74S/PRS).
