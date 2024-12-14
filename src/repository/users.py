from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User
from src.schemas import UserCreate


class UserRepository:
    """
    Repository class for managing user-related database operations.

    Attributes:
        db (AsyncSession): The asynchronous database session.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the UserRepository with a database session.

        Args:
            session (AsyncSession): The asynchronous database session.
        """
        self.db = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieve a user by their unique ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User | None: The user object if found, or None if no user matches the given ID.
        """
        stmt = select(User).filter_by(id=user_id)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User | None: The user object if found, or None if no user matches the given username.
        """
        stmt = select(User).filter_by(username=username)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email (str): The email address of the user to retrieve.

        Returns:
            User | None: The user object if found, or None if no user matches the given email.
        """
        stmt = select(User).filter_by(email=email)
        user = await self.db.execute(stmt)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate, avatar: str = None) -> User:
        """
        Create a new user in the database.

        Args:
            body (UserCreate): The data required to create the user.
            avatar (str, optional): The URL of the user's avatar. Defaults to None.

        Returns:
            User: The created user object.
        """
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            avatar=avatar
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def reset_password(self, user_id: int, password: str) -> User | None:
        """
        Reset the password of a user identified by their ID.

        Args:
            user_id (int): The ID of the user whose password is to be reset.
            password (str): The new password to be set for the user.

        Returns:
            User: The updated user object with the new password or None if the user does not exist.

        """
        user = await self.get_user_by_id(user_id)
        if user:
            user.hashed_password = password
            await self.db.commit()
            await self.db.refresh(user)

        return user

    async def refresh_token(self, user_id: int, token: str) -> User | None:
        """
        Reset refresh token of a user identified by their ID.

        Args:
            user_id (int): The ID of the user whose password is to be reset.
            token (str): The new refresh token to be set for the user.

        Returns:
            User: The updated user object with the new token or None if the user does not exist.

        """
        user = await self.get_user_by_id(user_id)
        if user:
            user.refresh_token = token
            await self.db.commit()
            await self.db.refresh(user)

        return user

    async def confirmed_email(self, email: str) -> None:
        """
        Mark a user's email as confirmed.

        Args:
            email (str): The email address of the user to confirm.

        Returns:
            None
        """
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.db.commit()

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Update the avatar URL for a user.

        Args:
            email (str): The email address of the user.
            url (str): The new avatar URL.

        Returns:
            User: The updated user object.
        """
        user = await self.get_user_by_email(email)
        user.avatar = url
        await self.db.commit()
        await self.db.refresh(user)
        return user
