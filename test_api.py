#!/usr/bin/env python3
"""
Simple test script to demonstrate the Flask API functionality.
Run this after starting the Flask server with: python app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_api():
    print("🚀 Testing Flask API...")
    print("=" * 50)
    
    # Test API info
    print("\n1. Testing API Info...")
    response = requests.get(f"{BASE_URL}/api")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test health check
    print("\n2. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Test get all users
    print("\n3. Testing Get All Users...")
    response = requests.get(f"{BASE_URL}/api/users")
    print(f"Status: {response.status_code}")
    print(f"Users count: {response.json()['count']}")
    
    # Test create new user
    print("\n4. Testing Create New User...")
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25,
        "city": "Test City"
    }
    response = requests.post(f"{BASE_URL}/api/users", json=new_user)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        user_data = response.json()['data']
        print(f"Created user ID: {user_data['id']}")
        user_id = user_data['id']
        
        # Test get specific user
        print("\n5. Testing Get Specific User...")
        response = requests.get(f"{BASE_URL}/api/users/{user_id}")
        print(f"Status: {response.status_code}")
        print(f"User name: {response.json()['data']['name']}")
        
        # Test update user
        print("\n6. Testing Update User...")
        update_data = {"age": 26, "city": "Updated City"}
        response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_data)
        print(f"Status: {response.status_code}")
        print(f"Updated age: {response.json()['data']['age']}")
    
    # Test get all products
    print("\n7. Testing Get All Products...")
    response = requests.get(f"{BASE_URL}/api/products")
    print(f"Status: {response.status_code}")
    print(f"Products count: {response.json()['count']}")
    
    # Test create new product
    print("\n8. Testing Create New Product...")
    new_product = {
        "name": "Test Product",
        "price": 49.99,
        "category": "Test Category",
        "stock": 10,
        "description": "A test product"
    }
    response = requests.post(f"{BASE_URL}/api/products", json=new_product)
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        product_data = response.json()['data']
        print(f"Created product ID: {product_data['id']}")
    
    # Test get all posts
    print("\n9. Testing Get All Posts...")
    response = requests.get(f"{BASE_URL}/api/posts")
    print(f"Status: {response.status_code}")
    print(f"Posts count: {response.json()['count']}")
    
    # Test like a post
    print("\n10. Testing Like Post...")
    response = requests.post(f"{BASE_URL}/api/posts/1/like")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        likes = response.json()['data']['likes']
        print(f"Post now has {likes} likes")
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the Flask server is running on http://localhost:5000")
        print("Start it with: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
