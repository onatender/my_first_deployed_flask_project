from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Sample data
users = [
    {
        "id": "1",
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 28,
        "city": "New York",
        "created_at": "2024-01-15T10:30:00Z"
    },
    {
        "id": "2", 
        "name": "Jane Smith",
        "email": "jane.smith@example.com",
        "age": 32,
        "city": "Los Angeles",
        "created_at": "2024-01-16T14:20:00Z"
    },
    {
        "id": "3",
        "name": "Mike Johnson",
        "email": "mike.johnson@example.com",
        "age": 25,
        "city": "Chicago",
        "created_at": "2024-01-17T09:15:00Z"
    }
]

products = [
    {
        "id": "1",
        "name": "Wireless Headphones",
        "price": 99.99,
        "category": "Electronics",
        "stock": 50,
        "description": "High-quality wireless headphones with noise cancellation",
        "created_at": "2024-01-10T08:00:00Z"
    },
    {
        "id": "2",
        "name": "Coffee Maker",
        "price": 79.99,
        "category": "Appliances",
        "stock": 25,
        "description": "Programmable coffee maker with timer",
        "created_at": "2024-01-12T11:30:00Z"
    },
    {
        "id": "3",
        "name": "Running Shoes",
        "price": 129.99,
        "category": "Sports",
        "stock": 100,
        "description": "Comfortable running shoes for all terrains",
        "created_at": "2024-01-14T16:45:00Z"
    }
]

posts = [
    {
        "id": "1",
        "title": "Getting Started with Flask",
        "content": "Flask is a lightweight web framework for Python. It's perfect for building APIs and web applications.",
        "author": "John Doe",
        "author_id": "1",
        "likes": 15,
        "created_at": "2024-01-18T12:00:00Z"
    },
    {
        "id": "2",
        "title": "Python Best Practices",
        "content": "Here are some best practices for writing clean and maintainable Python code.",
        "author": "Jane Smith",
        "author_id": "2",
        "likes": 23,
        "created_at": "2024-01-19T15:30:00Z"
    },
    {
        "id": "3",
        "title": "API Design Principles",
        "content": "Designing RESTful APIs requires careful consideration of endpoints, status codes, and data formats.",
        "author": "Mike Johnson",
        "author_id": "3",
        "likes": 8,
        "created_at": "2024-01-20T10:15:00Z"
    }
]

# Helper function to generate unique IDs
def generate_id():
    return str(uuid.uuid4())

# Helper function to get current timestamp
def get_current_timestamp():
    return datetime.utcnow().isoformat() + "Z"

# Routes for Users
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({
        "success": True,
        "data": users,
        "count": len(users)
    })

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return jsonify({
            "success": True,
            "data": user
        })
    return jsonify({
        "success": False,
        "message": "User not found"
    }), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({
            "success": False,
            "message": "Name and email are required"
        }), 400
    
    new_user = {
        "id": generate_id(),
        "name": data['name'],
        "email": data['email'],
        "age": data.get('age'),
        "city": data.get('city'),
        "created_at": get_current_timestamp()
    }
    
    users.append(new_user)
    return jsonify({
        "success": True,
        "data": new_user,
        "message": "User created successfully"
    }), 201

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400
    
    # Update user fields
    for key, value in data.items():
        if key in user and key != 'id' and key != 'created_at':
            user[key] = value
    
    return jsonify({
        "success": True,
        "data": user,
        "message": "User updated successfully"
    })

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    global users
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404
    
    users = [user for user in users if user['id'] != user_id]
    return jsonify({
        "success": True,
        "message": "User deleted successfully"
    })

# Routes for Products
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({
        "success": True,
        "data": products,
        "count": len(products)
    })

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = next((product for product in products if product['id'] == product_id), None)
    if product:
        return jsonify({
            "success": True,
            "data": product
        })
    return jsonify({
        "success": False,
        "message": "Product not found"
    }), 404

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('price'):
        return jsonify({
            "success": False,
            "message": "Name and price are required"
        }), 400
    
    new_product = {
        "id": generate_id(),
        "name": data['name'],
        "price": float(data['price']),
        "category": data.get('category', 'General'),
        "stock": data.get('stock', 0),
        "description": data.get('description', ''),
        "created_at": get_current_timestamp()
    }
    
    products.append(new_product)
    return jsonify({
        "success": True,
        "data": new_product,
        "message": "Product created successfully"
    }), 201

@app.route('/api/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    product = next((product for product in products if product['id'] == product_id), None)
    if not product:
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400
    
    # Update product fields
    for key, value in data.items():
        if key in product and key != 'id' and key != 'created_at':
            if key == 'price':
                product[key] = float(value)
            else:
                product[key] = value
    
    return jsonify({
        "success": True,
        "data": product,
        "message": "Product updated successfully"
    })

@app.route('/api/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    global products
    product = next((product for product in products if product['id'] == product_id), None)
    if not product:
        return jsonify({
            "success": False,
            "message": "Product not found"
        }), 404
    
    products = [product for product in products if product['id'] != product_id]
    return jsonify({
        "success": True,
        "message": "Product deleted successfully"
    })

# Routes for Posts
@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts"""
    return jsonify({
        "success": True,
        "data": posts,
        "count": len(posts)
    })

@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by ID"""
    post = next((post for post in posts if post['id'] == post_id), None)
    if post:
        return jsonify({
            "success": True,
            "data": post
        })
    return jsonify({
        "success": False,
        "message": "Post not found"
    }), 404

@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content') or not data.get('author_id'):
        return jsonify({
            "success": False,
            "message": "Title, content, and author_id are required"
        }), 400
    
    # Check if author exists
    author = next((user for user in users if user['id'] == data['author_id']), None)
    if not author:
        return jsonify({
            "success": False,
            "message": "Author not found"
        }), 400
    
    new_post = {
        "id": generate_id(),
        "title": data['title'],
        "content": data['content'],
        "author": author['name'],
        "author_id": data['author_id'],
        "likes": 0,
        "created_at": get_current_timestamp()
    }
    
    posts.append(new_post)
    return jsonify({
        "success": True,
        "data": new_post,
        "message": "Post created successfully"
    }), 201

@app.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    post = next((post for post in posts if post['id'] == post_id), None)
    if not post:
        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404
    
    post['likes'] += 1
    return jsonify({
        "success": True,
        "data": post,
        "message": "Post liked successfully"
    })

# General API info route
@app.route('/api', methods=['GET'])
def api_info():
    """Get API information"""
    return jsonify({
        "success": True,
        "message": "Welcome to the Flask API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/api/users",
            "products": "/api/products", 
            "posts": "/api/posts"
        },
        "sample_data": {
            "users_count": len(users),
            "products_count": len(products),
            "posts_count": len(posts)
        }
    })

# Health check route
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": get_current_timestamp()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
