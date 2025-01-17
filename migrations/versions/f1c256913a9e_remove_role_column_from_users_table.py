"""Remove role column from users table

Revision ID: f1c256913a9e
Revises: 98dd4bb79766
Create Date: 2024-12-14 22:05:45.427663

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1c256913a9e"
down_revision: Union[str, None] = "98dd4bb79766"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    user_role_enum = sa.Enum("USER", "ADMIN", "MODERATOR", name="userrole")
    user_role_enum.create(op.get_bind())

    op.add_column(
        "users",
        sa.Column("role", user_role_enum, nullable=False, server_default="USER"),
    )
    op.add_column(
        "users", sa.Column("refresh_token", sa.String(length=255), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "refresh_token")
    op.drop_column("users", "role")
    # ### end Alembic commands ###
