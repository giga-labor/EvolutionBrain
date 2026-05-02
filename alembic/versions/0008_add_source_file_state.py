"""add source_file_state table

Revision ID: 0008_add_source_file_state
Revises: 0007_add_goal_due_date
Create Date: 2026-05-02
"""

from alembic import op
import sqlalchemy as sa

revision = "0008_add_source_file_state"
down_revision = "0007_add_goal_due_date"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if "source_file_state" not in tables:
        op.create_table(
            "source_file_state",
            sa.Column("source_profile_id", sa.String(), sa.ForeignKey("source_profiles.id"), nullable=False),
            sa.Column("file_path", sa.String(), nullable=False),
            sa.Column("size_bytes", sa.BigInteger(), nullable=False, server_default="0"),
            sa.Column("mtime_ns", sa.BigInteger(), nullable=False, server_default="0"),
            sa.Column("content_hash", sa.String(), nullable=True),
            sa.Column("last_document_id", sa.String(), nullable=True),
            sa.Column("last_seen_at", sa.String(), nullable=True),
            sa.Column("status", sa.String(), nullable=False, server_default="active"),
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("source_profile_id", "file_path", name="uq_source_file_state_profile_path"),
        )
    indexes = {idx["name"] for idx in inspector.get_indexes("source_file_state")} if "source_file_state" in set(sa.inspect(bind).get_table_names()) else set()
    if "ix_source_file_state_source_profile_id" not in indexes:
        op.create_index("ix_source_file_state_source_profile_id", "source_file_state", ["source_profile_id"])


def downgrade() -> None:
    op.drop_index("ix_source_file_state_source_profile_id", table_name="source_file_state")
    op.drop_table("source_file_state")
