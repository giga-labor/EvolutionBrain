"""add document source_ref

Revision ID: 0005_add_document_source_ref
Revises: 0004_add_runtime_and_workflow_tables
Create Date: 2026-04-28
"""

from alembic import op
import sqlalchemy as sa

revision = "0005_add_document_source_ref"
down_revision = "0004_add_runtime_and_workflow_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("source_ref", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "source_ref")
