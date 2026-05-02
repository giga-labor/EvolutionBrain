"""add audit_entries

Revision ID: 0002_add_audit_entries
Revises: 0001_initial
Create Date: 2026-04-23
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_add_audit_entries"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "audit_entries",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("actor", sa.String(), nullable=True),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_audit_entries_entity_type", "audit_entries", ["entity_type"])
    op.create_index("ix_audit_entries_entity_id", "audit_entries", ["entity_id"])


def downgrade() -> None:
    op.drop_index("ix_audit_entries_entity_id", table_name="audit_entries")
    op.drop_index("ix_audit_entries_entity_type", table_name="audit_entries")
    op.drop_table("audit_entries")
