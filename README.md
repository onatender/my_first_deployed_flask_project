# Flask API with Sample Data

A comprehensive Flask REST API that provides sample data for users, products, and posts with full CRUD operations.

## Features

- **Users Management**: Create, read, update, and delete users
- **Products Management**: Manage product catalog with inventory tracking
- **Posts Management**: Handle blog posts with like functionality
- **CORS Enabled**: Cross-origin requests supported
- **Error Handling**: Comprehensive error responses
- **RESTful Design**: Follows REST API best practices

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### General Information

- **GET** `/api` - Get API information and statistics
- **GET** `/health` - Health check endpoint

### Users API

#### Get All Users
- **GET** `/api/users`
- **Response**: List of all users with count

#### Get User by ID
- **GET** `/api/users/{user_id}`
- **Response**: Single user data

#### Create User
- **POST** `/api/users`
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 28,
    "city": "New York"
  }
  ```
- **Required**: `name`, `email`

#### Update User
- **PUT** `/api/users/{user_id}`
- **Body**: Any user fields to update

#### Delete User
- **DELETE** `/api/users/{user_id}`

### Products API

#### Get All Products
- **GET** `/api/products`
- **Response**: List of all products with count

#### Get Product by ID
- **GET** `/api/products/{product_id}`
- **Response**: Single product data

#### Create Product
- **POST** `/api/products`
- **Body**:
  ```json
  {
    "name": "Wireless Headphones",
    "price": 99.99,
    "category": "Electronics",
    "stock": 50,
    "description": "High-quality wireless headphones"
  }
  ```
- **Required**: `name`, `price`

#### Update Product
- **PUT** `/api/products/{product_id}`
- **Body**: Any product fields to update

#### Delete Product
- **DELETE** `/api/products/{product_id}`

### Posts API

#### Get All Posts
- **GET** `/api/posts`
- **Response**: List of all posts with count

#### Get Post by ID
- **GET** `/api/posts/{post_id}`
- **Response**: Single post data

#### Create Post
- **POST** `/api/posts`
- **Body**:
  ```json
  {
    "title": "My Blog Post",
    "content": "This is the content of my blog post...",
    "author_id": "1"
  }
  ```
- **Required**: `title`, `content`, `author_id`

#### Like Post
- **POST** `/api/posts/{post_id}/like`
- **Response**: Updated post with incremented likes

## Sample Data

The API comes with pre-loaded sample data:

### Users (3 sample users)
- John Doe (john.doe@example.com)
- Jane Smith (jane.smith@example.com)
- Mike Johnson (mike.johnson@example.com)

### Products (3 sample products)
- Wireless Headphones ($99.99)
- Coffee Maker ($79.99)
- Running Shoes ($129.99)

### Posts (3 sample posts)
- "Getting Started with Flask"
- "Python Best Practices"
- "API Design Principles"

## Response Format

All API responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description"
}
```

## Example Usage

### Get all users
```bash
curl http://localhost:5000/api/users
```

### Create a new user
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 30,
    "city": "Boston"
  }'
```

### Get a specific product
```bash
curl http://localhost:5000/api/products/1
```

### Like a post
```bash
curl -X POST http://localhost:5000/api/posts/1/like
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side errors

## Development

The application runs in debug mode by default. For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure proper environment variables

## Dependencies

- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Werkzeug**: WSGI toolkit

## License

This project is open source and available under the MIT License.
