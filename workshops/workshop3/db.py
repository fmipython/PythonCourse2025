"""
Async Database Module with CRUD Operations
Reusable by both Flask and FastAPI applications
"""

import hashlib
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy import delete
from db_models import Base, User, Publication


class DatabaseService:
    """Async database manager for CRUD operations"""

    def __init__(self, database_url: str = "sqlite+aiosqlite:///./workshop.db"):
        """
        Initialize database connection
        Args:
            database_url: SQLAlchemy database URL (must support async)
        """
        self.engine = create_async_engine(database_url, echo=False)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_tables(self):
        """Create all tables defined in models"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # preload database with test admin user
        await self._preload_data()

    async def drop_tables(self):
        """Drop all tables - useful for testing"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def close(self):
        """Close database connection"""
        await self.engine.dispose()

    async def _preload_data(self):
        """Preload database with initial data"""
        existing_user = await self.get_user_by_username("test_admin")
        if not existing_user:
            await self.create_user(
                username="test_admin",
                email="test_admin@example.com",
                password="testing123",
                is_admin=True,
            )
            print("✓ Preloaded database with test_admin user")

    # ==================== USER CRUD OPERATIONS ====================

    async def create_user(
        self, username: str, email: str, password: str, is_admin: bool = False
    ) -> User:
        """
        Create a new user
        Args:
            username: Unique username
            email: User email
            password: Plain text password (will be hashed)
            is_admin: Whether the user has admin privileges (default: False)
        Returns:
            Created User object
        """
        async with self.async_session() as session:
            # Simple password hashing (for demo purposes - use bcrypt/passlib in production)
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                is_admin=is_admin,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user(self, user_id: int) -> User | None:
        """Get user by ID"""
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username"""
        async with self.async_session() as session:
            result = await session.execute(
                select(User).where(User.username == username)
            )
            return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""
        async with self.async_session() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> Sequence[User]:
        """Get all users with pagination"""
        async with self.async_session() as session:
            result = await session.execute(select(User).offset(skip).limit(limit))
            return result.scalars().all()

    async def update_user(self, user_id: int, **kwargs) -> User | None:
        """
        Update user fields
        Args:
            user_id: User ID to update
            **kwargs: Fields to update (username, email, password)
        Returns:
            Updated User object or None if not found
        """
        async with self.async_session() as session:
            # Hash password if provided
            if "password" in kwargs:
                kwargs["password_hash"] = hashlib.sha256(
                    kwargs.pop("password").encode()
                ).hexdigest()

            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                await session.commit()
                await session.refresh(user)
            return user

    async def delete_user(self, user_id: int) -> bool:
        """
        Delete user by ID
        Returns:
            True if deleted, False if not found
        """
        async with self.async_session() as session:
            result = await session.execute(delete(User).where(User.id == user_id))
            await session.commit()
            return result.rowcount > 0  # type: ignore

    async def authenticate_user(self, username: str, password: str) -> User | None:
        """
        Authenticate user by username and password
        Returns:
            User object if credentials are valid, None otherwise
        """
        async with self.async_session() as session:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            result = await session.execute(
                select(User).where(
                    User.username == username, User.password_hash == password_hash
                )
            )
            return result.scalar_one_or_none()

    # ==================== PUBLICATION CRUD OPERATIONS ====================

    async def create_publication(
        self,
        title: str,
        content: str,
        owner_id: int,
    ) -> Publication:
        """
        Create a new publication
        Args:
            title: Publication title
            content: Publication content
            owner_id: ID of the user who owns this publication
        Returns:
            Created Publication object
        """
        async with self.async_session() as session:
            publication = Publication(
                title=title,
                content=content,
                owner_id=owner_id,
            )
            session.add(publication)
            await session.commit()
            await session.refresh(publication)
            return publication

    async def get_publication(self, publication_id: int) -> Publication | None:
        """Get publication by ID"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Publication).where(Publication.id == publication_id)
            )
            return result.scalar_one_or_none()

    async def get_all_publications(
        self, skip: int = 0, limit: int = 100
    ) -> Sequence[Publication]:
        """Get all publications with pagination"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Publication).offset(skip).limit(limit)
            )
            return result.scalars().all()

    async def get_publications_by_owner(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Publication]:
        """Get all publications owned by a specific user"""
        async with self.async_session() as session:
            result = await session.execute(
                select(Publication)
                .where(Publication.owner_id == owner_id)
                .offset(skip)
                .limit(limit)
            )
            return result.scalars().all()

    async def update_publication(
        self, publication_id: int, **kwargs
    ) -> Publication | None:
        """
        Update publication fields
        Args:
            publication_id: Publication ID to update
            **kwargs: Fields to update (name, description, price, quantity)
        Returns:
            Updated Publication object or None if not found
        """
        async with self.async_session() as session:
            result = await session.execute(
                select(Publication).where(Publication.id == publication_id)
            )
            publication = result.scalar_one_or_none()

            if publication:
                for key, value in kwargs.items():
                    if hasattr(publication, key):
                        setattr(publication, key, value)
                await session.commit()
                await session.refresh(publication)
            return publication

    async def delete_publication(self, publication_id: int) -> bool:
        """
        Delete publication by ID
        Returns:
            True if deleted, False if not found
        """
        async with self.async_session() as session:
            result = await session.execute(
                delete(Publication).where(Publication.id == publication_id)
            )
            await session.commit()
            return result.rowcount > 0  # type: ignore
