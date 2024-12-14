from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, func, Date, Boolean, Enum as SqlEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey, UniqueConstraint
from enum import Enum


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models. Inherits from DeclarativeBase.
    This class serves as a base for all tables and model classes.
    """

    pass


class Contact(Base):
    """
    Contact represents a user's contact information in the database.

    Attributes:
        id (int): The unique identifier for the contact.
        first_name (str): The first name of the contact.
        last_name (str): The last name of the contact.
        email (str): The email address of the contact. Must be unique.
        phone_number (str): The phone number of the contact.
        birthday (datetime.date): The birthday of the contact.
        additional_info (str): Any additional information about the contact.
        created_at (datetime): The timestamp when the contact was created. Defaults to the current time.
        updated_at (datetime): The timestamp when the contact was last updated. Automatically updated on modification.
        user_id (int): The foreign key referencing the associated user.
        user (User): The relationship to the `User` model.
    """

    __tablename__ = "contacts"
    __table_args__ = (UniqueConstraint("email", "user_id", name="unique_email_user"),)

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=False)
    birthday = Column(Date, nullable=True)
    additional_info = Column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        "created_at", DateTime, default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
    user_id = Column(
        "user_id", ForeignKey("users.id", ondelete="CASCADE"), default=None
    )
    user = relationship("User", backref="contacts")


class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(Base):
    """
    User represents a system user, storing their authentication and profile details.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The unique username for the user.
        email (str): The unique email address of the user.
        hashed_password (str): The hashed password of the user.
        created_at (datetime): The timestamp when the user was created. Defaults to the current time.
        avatar (str): A URL to the user's avatar image (optional).
        confirmed (bool): A flag indicating whether the user's email has been confirmed.
        role (UserRole): The user role.
        refresh_token: The refresh token for the user.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    role = Column(SqlEnum(UserRole), default=UserRole.USER, nullable=False)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
