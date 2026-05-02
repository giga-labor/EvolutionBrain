"""add cognitive core tables

Revision ID: 0003_add_cognitive_core_tables
Revises: 0002_add_audit_entries
Create Date: 2026-04-27
"""

from alembic import op
import sqlalchemy as sa

revision = "0003_add_cognitive_core_tables"
down_revision = "0002_add_audit_entries"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "concepts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.7"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_concepts_name", "concepts", ["name"])

    op.create_table(
        "relations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("source_id", sa.String(), nullable=False),
        sa.Column("target_id", sa.String(), nullable=False),
        sa.Column("relation_type", sa.String(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.7"),
        sa.Column("evidence", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_relations_source_id", "relations", ["source_id"])
    op.create_index("ix_relations_target_id", "relations", ["target_id"])
    op.create_index("ix_relations_relation_type", "relations", ["relation_type"])

    op.create_table(
        "memory_items",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("object_type", sa.String(), nullable=False),
        sa.Column("object_id", sa.String(), nullable=False),
        sa.Column("layer", sa.String(), nullable=False, server_default="active"),
        sa.Column("relevance_score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.7"),
        sa.Column("access_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_accessed_at", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_memory_items_object_type", "memory_items", ["object_type"])
    op.create_index("ix_memory_items_object_id", "memory_items", ["object_id"])

    op.create_table(
        "goals",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("project_id", sa.String(), sa.ForeignKey("projects.id"), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("goals")
    op.drop_index("ix_memory_items_object_id", table_name="memory_items")
    op.drop_index("ix_memory_items_object_type", table_name="memory_items")
    op.drop_table("memory_items")
    op.drop_index("ix_relations_relation_type", table_name="relations")
    op.drop_index("ix_relations_target_id", table_name="relations")
    op.drop_index("ix_relations_source_id", table_name="relations")
    op.drop_table("relations")
    op.drop_index("ix_concepts_name", table_name="concepts")
    op.drop_table("concepts")
