"""
Flask REST API Application
Demonstrates CRUD operations with authentication using Flask
"""

import asyncio
from functools import wraps
from flask import Flask, request, jsonify, g
from werkzeug.exceptions import HTTPException
import base64
from db import DatabaseService


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

db = DatabaseService()


# ==================== Helper Functions ====================


def async_route(f):
    """Decorator to handle async route handlers in Flask"""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def get_auth_credentials():
    """Extract username and password from Basic Auth header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Basic "):
        return None, None

    try:
        # Decode base64 credentials
        encoded_credentials = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded.split(":", 1)
        return username, password
    except Exception:
        return None, None


def user_to_dict(user, include_password=False):
    """Convert User model to dictionary"""
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_admin": user.is_admin,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
    if include_password:
        data["password_hash"] = user.password_hash
    return data


def publication_to_dict(publication):
    """Convert Publication model to dictionary"""
    return {
        "id": publication.id,
        "title": publication.title,
        "content": publication.content,
        "owner_id": publication.owner_id,
        "created_at": (
            publication.created_at.isoformat() if publication.created_at else None
        ),
        "updated_at": (
            publication.updated_at.isoformat() if publication.updated_at else None
        ),
    }


def require_auth(f):
    """Decorator to require authentication for endpoints"""

    @wraps(f)
    async def decorated_function(*args, **kwargs):
        username, password = get_auth_credentials()

        if not username or not password:
            return jsonify({"error": "Authentication required"}), 401

        user = await db.authenticate_user(username, password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Store authenticated user in request context
        g.current_user = user
        return await f(*args, **kwargs)

    return decorated_function


def require_admin_auth(f):
    """Decorator to require admin authentication for endpoints"""

    @wraps(f)
    async def decorated_function(*args, **kwargs):
        username, password = get_auth_credentials()

        if not username or not password:
            return jsonify({"error": "Authentication required"}), 401

        user = await db.authenticate_user(username, password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Check if user is admin
        if not user.is_admin:
            return jsonify({"error": "Admin privileges required"}), 403

        # Store authenticated user in request context
        g.current_user = user
        return await f(*args, **kwargs)

    return decorated_function


# ==================== Error Handlers ====================


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Handle HTTP exceptions"""
    return jsonify({"error": e.description}), e.code


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected exceptions"""
    app.logger.error(f"Unexpected error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500


# ==================== Startup/Shutdown ====================


@app.before_request
@async_route
async def before_first_request():
    """Initialize database tables"""
    if not hasattr(app, "db_initialized"):
        await db.create_tables()
        app.db_initialized = True


# ==================== USER ENDPOINTS ====================


@app.route("/users", methods=["POST"])
@async_route
async def create_user():
    """Create a new user"""
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["username", "email", "password"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return (
            jsonify({"error": f'Missing required fields: {", ".join(missing_fields)}'}),
            400,
        )

    username, email, password = data["username"], data["email"], data["password"]

    user_with_username = await db.get_user_by_username(username)
    if user_with_username is not None:
        return jsonify({"error": "Username already exists"}), 400

    user_with_email = await db.get_user_by_email(email)
    if user_with_email is not None:
        return jsonify({"error": "Email already exists"}), 400

    new_user = await db.create_user(
        username=username, email=email, password=password, is_admin=False
    )

    return jsonify(user_to_dict(new_user)), 201


@app.route("/users/<int:user_id>", methods=["GET"])
@async_route
@require_auth
async def get_user(user_id):
    """Get user by ID"""
    user = await db.get_user(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user_to_dict(user))


@app.route("/users", methods=["GET"])
@async_route
@require_admin_auth
async def get_all_users():
    """Get all users with pagination (admin only)"""
    skip = request.args.get("skip", 0, type=int)
    limit = request.args.get("limit", 100, type=int)

    users = await db.get_all_users(skip=skip, limit=limit)
    return jsonify([user_to_dict(user) for user in users])


@app.route("/users/<int:user_id>", methods=["PUT"])
@async_route
@require_auth
async def update_user(user_id):
    """Update user (own profile or admin can update any)"""
    if g.current_user.id != user_id and not g.current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Filter allowed fields
    allowed_fields = ["username", "email", "password"]
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    try:
        user = await db.update_user(user_id, **update_data)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user_to_dict(user))
    except Exception as e:
        return jsonify({"error": f"Failed to update user: {str(e)}"}), 400


@app.route("/users/<int:user_id>", methods=["DELETE"])
@async_route
@require_auth
async def delete_user(user_id):
    """Delete user (own account or admin can delete any)"""
    if g.current_user.id != user_id and not g.current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403

    success = await db.delete_user(user_id)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200


# ==================== PUBLICATION ENDPOINTS ====================


# POST /publications

# GET /publications/<publication_id>

# GET /publications?owner_id=&skip=&limit=

# PUT /publications/<publication_id>

# DELETE /publications/<publication_id>


if __name__ == "__main__":
    app.run(debug=True, port=5000)
