"""
FastAPI App Tests
Comprehensive tests for FastAPI REST API endpoints using in-memory SQLite database
"""

import pytest
import base64
from httpx import AsyncClient, ASGITransport
from fastapi_app import app, get_db
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
async def client(test_db):
    """Create FastAPI test client"""

    # override the get_db dependency to use test database
    async def override_get_db():
        return test_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


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


@pytest.mark.asyncio
async def test_create_user(client):
    """Test user creation"""
    response = await client.post(
        "/users",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "secure123",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["is_admin"] == False  # Verify user is not admin by default
    assert "id" in data
    assert "password" not in data  # Password should not be returned


@pytest.mark.asyncio
async def test_create_user_missing_fields(client):
    """Test user creation with missing fields"""
    response = await client.post("/users", json={"username": "newuser"})

    assert response.status_code == 422  # FastAPI validation error


@pytest.mark.asyncio
async def test_create_user_invalid_email(client):
    """Test user creation with invalid email"""
    response = await client.post(
        "/users",
        json={"username": "newuser", "email": "not-an-email", "password": "secure123"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_user(client, sample_user):
    """Test getting user by ID"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.get(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_user.id
    assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_unauthorized(client, sample_user):
    """Test getting user without authentication"""
    response = await client.get(f"/users/{sample_user.id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_wrong_credentials(client, sample_user):
    """Test getting user with wrong credentials"""
    auth_header = get_auth_header("testuser", "wrongpassword")
    response = await client.get(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_user_not_found(client, sample_user):
    """Test getting non-existent user"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.get("/users/9999", headers=auth_header)

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_users(client, admin_user):
    """Test getting all users (admin only)"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = await client.get("/users", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_all_users_non_admin(client, sample_user):
    """Test that non-admin users cannot get all users"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.get("/users", headers=auth_header)

    assert response.status_code == 403  # Forbidden for non-admin users


@pytest.mark.asyncio
async def test_get_all_users_pagination(client, admin_user):
    """Test getting users with pagination (admin only)"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = await client.get("/users?skip=0&limit=10", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_update_user(client, sample_user):
    """Test updating user"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "updated@example.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "updated@example.com"


@pytest.mark.asyncio
async def test_update_user_unauthorized(client, sample_user, test_db):
    """Test updating another user's profile (non-admin)"""
    # Create another user
    await test_db.create_user("otheruser", "other@example.com", "pass123")

    # Try to update original user with different credentials
    auth_header = get_auth_header("otheruser", "pass123")
    response = await client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "hacker@example.com"},
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_user_as_admin(client, sample_user, admin_user):
    """Test admin can update any user's profile"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = await client.put(
        f"/users/{sample_user.id}",
        headers=auth_header,
        json={"email": "admin_updated@example.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin_updated@example.com"


@pytest.mark.asyncio
async def test_update_user_no_fields(client, sample_user):
    """Test updating user with no fields"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.put(
        f"/users/{sample_user.id}", headers=auth_header, json={}
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_delete_user(client, sample_user):
    """Test deleting user"""
    auth_header = get_auth_header("testuser", "password123")
    response = await client.delete(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


@pytest.mark.asyncio
async def test_delete_user_as_admin(client, sample_user, admin_user):
    """Test admin can delete any user"""
    auth_header = get_auth_header("adminuser", "admin123")
    response = await client.delete(f"/users/{sample_user.id}", headers=auth_header)

    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# ==================== PUBLICATION TESTS ====================

# TODO: Add publication tests here
