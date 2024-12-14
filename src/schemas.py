from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.database.models import UserRole


class ContactBase(BaseModel):
    """
    ContactBase is the base model that represents the required fields to create or update a contact.

    Attributes:
        first_name (str): The first name of the contact. Maximum length is 50 characters.
        last_name (str): The last name of the contact. Maximum length is 50 characters.
        email (EmailStr): The email address of the contact.
        phone_number (str): The phone number of the contact.
        birthday (date): The birthday of the contact.
        additional_info (Optional[str]): Any additional information about the contact, optional.
    """

    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info: Optional[str]


class ContactUpdate(BaseModel):
    """
    ContactUpdate is used for updating an existing contact. All fields are optional.

    Attributes:
        first_name (Optional[str]): The updated first name of the contact, if provided.
        last_name (Optional[str]): The updated last name of the contact, if provided.
        email (Optional[EmailStr]): The updated email address of the contact, if provided.
        phone_number (Optional[str]): The updated phone number of the contact, if provided.
        birthday (Optional[date]): The updated birthday of the contact, if provided.
        additional_info (Optional[str]): Any additional updated information about the contact, if provided.
    """

    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    birthday: Optional[date]
    additional_info: Optional[str]


class ContactResponse(ContactBase):
    """
    ContactResponse extends ContactBase to include the ID field, used for returning the contact data in API responses.

    Attributes:
        id (int): The unique identifier for the contact.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    """
    User represents a system user, containing essential user information.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        avatar (str): The URL to the user's avatar image.
        role (UserRole): User role of the new user.
    """

    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    UserCreate is used for creating a new user. It includes the necessary fields for registration.

    Attributes:
        username (str): The username of the new user.
        email (str): The email address of the new user.
        password (str): The password of the new user.
        role (UserRole): User role of the new user.
    """

    username: str
    email: str
    password: str
    role: UserRole


class Token(BaseModel):
    """
    Token represents an authentication token returned upon user login.

    Attributes:
        access_token (str): The authentication token.
        refresh_token (str): The refresh token.
        token_type (str): The type of the token (e.g., 'bearer').
    """

    access_token: str
    refresh_token: str
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class RequestEmail(BaseModel):
    """
    RequestEmail is used for processing requests related to email.

    Attributes:
        email (EmailStr): The email address being requested.
    """

    email: EmailStr


class ResetPassword(BaseModel):
    """
    ResetPassword is used  for handling password reset requests.

    Attributes:
        email (EmailStr): The email address of the user requesting the password reset.
        password (str): The new password for the user
    """

    email: EmailStr
    password: str
