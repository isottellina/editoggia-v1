"""Create the bare minimum

Revision ID: ed2036a1d0c0
Revises: 15e1c1a1278e
Create Date: 2022-01-31 18:40:06.851185

"""
import sqlalchemy as sa
from alembic import op

from editoggia.models import Fandom, FandomCategory, Permission, Role
from editoggia.models.user import PermissionsRoles

# revision identifiers, used by Alembic.
revision = "ed2036a1d0c0"
down_revision = "15e1c1a1278e"
branch_labels = None
depends_on = None


permissions = [
    ("admin.ACCESS_ADMIN_INTERFACE", "Can access the admin interface"),
    ("mod.ACCESS_TAG_INTERFACE", "Can access the interface to manage tag and fandoms."),
]

roles = [
    (
        "Administrator",
        "Administrator of the website.",
        (
            "admin.ACCESS_ADMIN_INTERFACE",
            "mod.ACCESS_TAG_INTERFACE",
        ),
    ),
    ("Moderator", "Moderator.", ("mod.ACCESS_TAG_INTERFACE",)),
]


def upgrade():
    bind = op.get_bind()

    for category in [
        "Anime",
        "Books",
        "Cartoons",
        "Movies",
        "Video Games",
        "TV Shows",
        "Other",
    ]:
        op.execute(sa.insert(FandomCategory).values(name=category))

    other_id = bind.scalar(sa.select(FandomCategory.id).filter_by(name="Other"))

    op.execute(
        sa.insert(Fandom).values(
            name="Original Work",
            category_id=other_id,
            waiting_mod=False,
        )
    )

    # Create permissions
    for permission in permissions:
        name, description = permission
        op.execute(sa.insert(Permission).values(name=name, description=description))

    # Create roles
    for role in roles:
        name, description, role_permissions = role
        role_id = bind.scalar(
            sa.insert(Role)
            .values(name=name, description=description)
            .returning(Role.id)
        )

        for permission_name in role_permissions:
            permission_id = bind.scalar(
                sa.select(Permission).where(Permission.name == permission_name)
            )
            op.execute(
                sa.insert(PermissionsRoles).values(
                    perm_id=permission_id, role_id=role_id
                )
            )


def downgrade():
    pass
