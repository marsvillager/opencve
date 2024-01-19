"""Add endpoints table and results table

Revision ID: 6a3664d4b2c3
Revises: 1c7aecfc5f6e
Create Date: 2024-01-17 11:45:46.044921

"""

# revision identifiers, used by Alembic.
revision = "6a3664d4b2c3"
down_revision = "1c7aecfc5f6e"

from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType, JSONType
from opencve.extensions import db
from sqlalchemy.dialects import postgresql

def upgrade():
    
    op.create_table(
        "endpoints",
        sa.Column("id", UUIDType(binary=False), nullable=False),
        sa.Column("mac", sa.String(), nullable=True),
        sa.Column("json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("mac"),
    )
    
    op.create_table(
        "results",
        sa.Column("endpoint_id", UUIDType(binary=False), nullable=False),
        sa.Column("cve_id", UUIDType(binary=False), nullable=False),
        sa.Column("reason", sa.String(), nullable=False),
        sa.Column("possibility", db.Integer, nullable=False),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoints.id"],
        ),
        sa.ForeignKeyConstraint(
            ["cve_id"],
            ["cves.id"],
        ),
        sa.PrimaryKeyConstraint("endpoint_id", "cve_id"),
    )


def downgrade():
    op.drop_table("results")
    op.drop_table("endpoints")
