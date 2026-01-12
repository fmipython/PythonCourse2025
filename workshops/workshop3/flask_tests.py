"""
Flask App Tests
Comprehensive tests for Flask REST API endpoints using in-memory SQLite database
"""

import pytest
import asyncio
import base64
from flask_app import app
from db import DatabaseService

# =========
# FIXTURES
# =========

@pytest.fixture
async def test_db():
    """Create an in-memory database for testing"""
    db = DatabaseService("sqlite+aiosqlite:///:memory:")
    await db.create_tables()
    yield db
    await db.close()


@pytest.fixture
def client(test_db):
    """Create Flask test client"""
    app.config["TESTING"] = True

    # replace the app's database with test database
    import flask_app
    flask_app.db = test_db
    # това заменя стойността на глобалната променлива `db` в модула `flask_app`

    with app.test_client() as client:
        yield client


@pytest.fixture
async def sample_user(test_db):
    """Create a sample non-admin user for testing"""
    user = await test_db.create_user(
        username="testuser", email="test@example.com", password="password123"
    )
    return user


@pytest.fixture
async def admin_user(test_db):
    """Create an admin user for testing"""
    user = await test_db.create_user(
        username="adminuser",
        email="admin@example.com",
        password="admin123",
        is_admin=True,
    )
    return user


@pytest.fixture
async def sample_publication(test_db, sample_user):
    """Create a sample publication for testing"""
    publication = await test_db.create_publication(
        title="Test Publication",
        content="This is a test publication content.",
        owner_id=sample_user.id,
    )
    return publication


def get_auth_header(username, password):
    """Generate Basic Auth header"""
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


# ==================== USER TESTS ====================


def test_create_user(client):
    """Test user creation"""
    response = client.post(
        "/users",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure123",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["is_admin"] == False  # Verify user is not admin by default
    assert "id" in data
    assert "password" not in data  # Password should not be returned


def test_create_user_missing_fields(client):
    """Test user creation with missing fields"""
    response = client.post("/users", json={"username": "newuser"})

    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_create_user_ignores_admin_field(client):
    """Test that is_admin field is ignored in user creation"""
    response = client.post(
        "/users",
        json={
            "username": "wannabe_admin",
            "email": "wannabe@example.com",
            "password": "secure123",
            "is_admin": True,  # This should be ignored
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["is_admin"] == False  # Should be False despite request


def test_get_user(client, sample_user):
    """Test getting user by ID"""
    auth_header = get_auth_header("testuser", "password123")
    response = client.get(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == sample_user.id
    assert data["username"] == "testuser"


def test_get_user_unauthorized(client, sample_user):
    """Test getting user without authentication"""
    response = client.get(f"/users/{sample_user.id}")

    assert response.status_code == 401


def test_get_user_not_found(client, sample_user):
    """Test getting non-existent user"""
    auth_header = get_auth_header("testuser", "password123")
    response = client.get("/users/9999", headers=auth_header)

    assert response.status_code == 404


def test_get_all_users(client, admin_user):
    """Test getting all users (admin only)"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = client.get("/users", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_all_users_non_admin(client, sample_user):
    """Test that non-admin users cannot get all users"""
    auth_header = get_auth_header("testuser", "password123")
    response = client.get("/users", headers=auth_header)

    assert response.status_code == 403  # Forbidden for non-admin users


def test_update_user(client, sample_user):
    """Test updating user"""
    auth_header = get_auth_header("testuser", "password123")
    response = client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "updated@example.com"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "updated@example.com"


def test_update_user_unauthorized(client, sample_user, test_db):
    """Test updating another user's profile (non-admin)"""
    # Create another user
    asyncio.run(test_db.create_user("otheruser", "other@example.com", "pass123"))

    # Try to update original user with different credentials
    auth_header = get_auth_header("otheruser", "pass123")
    response = client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "hacker@example.com"},
    )

    assert response.status_code == 403


def test_update_user_as_admin(client, sample_user, admin_user):
    """Test admin can update any user's profile"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "admin_updated@example.com"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["email"] == "admin_updated@example.com"


def test_delete_user(client, sample_user):
    """Test deleting user"""
    auth_header = get_auth_header("testuser", "password123")
    response = client.delete(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_delete_user_as_admin(client, sample_user, admin_user):
    """Test admin can delete any user"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = client.delete(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


# ==================== PUBLICATION TESTS ====================


# TODO: Add publication tests here