# flask-sqlalchemy-project

A sample project demonstrating Python with Flask and SQLAlchemy. It showcases basic CRUD (Create, Read, Update, Delete) operations on a `User` resource via a REST API backed by SQLite.

## Project Structure

```
flask-sqlalchemy-project/
├── app.py            # Flask application with CRUD routes
├── models.py         # SQLAlchemy User model
├── requirements.txt  # Python dependencies
└── tests/
    └── test_app.py   # Pytest tests for all CRUD operations
```

## Setup

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint          | Description        |
|--------|-------------------|--------------------|
| GET    | `/users`          | List all users     |
| GET    | `/users/<id>`     | Get a user by ID   |
| POST   | `/users`          | Create a new user  |
| PUT    | `/users/<id>`     | Update a user      |
| DELETE | `/users/<id>`     | Delete a user      |

### Example Requests

```bash
# Create a user
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "email": "alice@example.com"}'

# List all users
curl http://127.0.0.1:5000/users

# Update a user
curl -X PUT http://127.0.0.1:5000/users/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice Smith"}'

# Delete a user
curl -X DELETE http://127.0.0.1:5000/users/1
```

## Run Tests

```bash
pytest tests/
```