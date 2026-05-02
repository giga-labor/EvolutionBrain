"""add source profiles

Revision ID: 0006_add_source_profiles
Revises: 0005_add_document_source_ref
Create Date: 2026-04-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0006_add_source_profiles"
down_revision = "0005_add_document_source_ref"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "source_profiles",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("source_ref", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_source_profiles_name", "source_profiles", ["name"])
    op.create_index("ix_source_profiles_source_type", "source_profiles", ["source_type"])


def downgrade() -> None:
    op.drop_index("ix_source_profiles_source_type", table_name="source_profiles")
    op.drop_index("ix_source_profiles_name", table_name="source_profiles")
    op.drop_table("source_profiles")
