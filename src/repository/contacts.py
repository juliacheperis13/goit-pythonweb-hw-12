from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact, User
from src.schemas import ContactBase

from sqlalchemy.sql.expression import and_, extract, or_

from datetime import date, timedelta


class ContactRepository:
    def __init__(self, session: AsyncSession):
        """
        Initialize a ContactRepository.

        Args:
            session: An AsyncSession object connected to the database.
        """
        self.db = session

    async def get_contacts(
        self,
        user: User,
        skip: int = 0,
        limit: int = 10,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
    ) -> List[Contact]:
        """
        Get a list of Notes owned by `user` with pagination.

        Args:
            skip: The number of Contacts to skip.
            limit: The maximum number of Contacts to return.
            user: The owner of the Contacts to retrieve.
            first_name: The first name of the Contact to return.
            last_name: The last name of the Contact to return.
            email: The email address of the Contact to return.

        Returns:
            A list of Contacts.
        """

        filters = []

        if first_name:
            filters.append(Contact.first_name.like(f"%{first_name}%"))
        if last_name:
            filters.append(Contact.last_name.like(f"%{last_name}%"))
        if email:
            filters.append(Contact.email.like(f"%{email}%"))

        # Build the query dynamically
        stmt = (
            select(Contact)
            .filter_by(user=user)
            .where(and_(*filters))
            .offset(skip)
            .limit(limit)
        )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int, user: User) -> Contact | None:
        """
        Get a Contact by its id.

        Args:
            contact_id: The id of the Contact to retrieve.
            user: The owner of the Contact to retrieve.

        Returns:
            The Contact with the specified id, or None if no such Contact exists.
        """
        stmt = select(Contact).filter_by(id=contact_id, user=user)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactBase, user: User) -> Contact:
        """
        Create a new Contact with the given attributes.

        Args:
            body: A ContactBase with the attributes to assign to the Contact.
            user: The User who owns the Contact.

        Returns:
            A Contact with the assigned attributes.
        """

        contact = Contact(**body.model_dump(exclude_unset=True), user=user)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactBase, user: User
    ) -> Contact | None:
        """
        Update a new Contact with the given attributes.

        Args:
            body: A ContactBase with the attributes to assign to the Contact.
            user: The User who owns the Contact.

        Returns:
            A Contact with the assigned attributes.
        """

        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            contact.first_name = body.first_name
            contact.last_name = body.last_name
            contact.birthday = body.birthday
            contact.additional_info = body.additional_info
            contact.email = body.email
            contact.phone_number = body.phone_number

            await self.db.commit()
            await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int, user: User) -> Contact | None:
        """
        Delete a Contact by its id.

        Args:
            contact_id: The id of the Contact to delete.
            user: The owner of the Contact to delete.

        Returns:
            The deleted Contact, or None if no Contact with the given id exists.
        """

        contact = await self.get_contact_by_id(contact_id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self, user: User, days: int = 7) -> List:
        """
        Get Contacts to have upcoming birthdays for specified days.

        Args:
            days: The number of days to look back.
            user: The owner of the Contact to find.

        Returns:
            The list of contacts that have upcoming birthdays.
        """

        today = date.today()
        target_date = today + timedelta(days=days)

        if target_date.year == today.year:
            # Query stays within the same year
            stmt = (
                select(Contact)
                .filter_by(user=user)
                .filter(
                    or_(
                        and_(
                            extract("month", Contact.birthday) == today.month,
                            extract("day", Contact.birthday) >= today.day,
                        ),
                        and_(
                            extract("month", Contact.birthday) == target_date.month,
                            extract("day", Contact.birthday) <= target_date.day,
                        ),
                        and_(
                            extract("month", Contact.birthday) > today.month,
                            extract("month", Contact.birthday) < target_date.month,
                        ),
                    )
                )
            )
        else:
            # Range crosses into the next year
            stmt = select(Contact).filter(
                or_(
                    # Birthdays in the current year
                    and_(
                        extract("month", Contact.birthday) == today.month,
                        extract("day", Contact.birthday) >= today.day,
                    ),
                    and_(
                        extract("month", Contact.birthday) > today.month,
                    ),
                    # Birthdays in the next year
                    and_(
                        extract("month", Contact.birthday) == target_date.month,
                        extract("day", Contact.birthday) <= target_date.day,
                    ),
                    and_(
                        extract("month", Contact.birthday) < target_date.month,
                    ),
                )
            )

        result = await self.db.execute(stmt)

        return result.scalars().all()
