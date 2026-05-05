"""seed security policies for identity and credential anti-fraud

Revision ID: 0009_seed_security_policies
Revises: 0008_add_source_file_state
Create Date: 2026-05-05
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa

revision = "0009_seed_security_policies"
down_revision = "0008_add_source_file_state"
branch_labels = None
depends_on = None


def _now_utc_naive() -> datetime:
    # Keep compatible with existing SQLite datetime values stored without timezone suffix.
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _upsert_security_note(
    conn: sa.Connection,
    *,
    title: str,
    body: str,
    timestamp: datetime,
) -> tuple[str, str]:
    select_sql = sa.text(
        """
        SELECT id
        FROM notes
        WHERE title = :title AND status = 'active'
        ORDER BY updated_at DESC
        LIMIT 1
        """
    )
    row = conn.execute(select_sql, {"title": title}).mappings().first()
    if row:
        note_id = row["id"]
        conn.execute(
            sa.text(
                """
                UPDATE notes
                SET body_markdown = :body,
                    note_type = 'security_policy',
                    source_type = 'system',
                    epistemic_type = 'policy',
                    confidence = 1.0,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {"body": body, "updated_at": timestamp, "id": note_id},
        )
        return note_id, "updated"

    note_id = str(uuid.uuid4())
    conn.execute(
        sa.text(
            """
            INSERT INTO notes (
                id, document_id, note_type, title, body_markdown, source_type,
                status, epistemic_type, confidence, created_at, updated_at
            )
            VALUES (
                :id, NULL, 'security_policy', :title, :body, 'system',
                'active', 'policy', 1.0, :created_at, :updated_at
            )
            """
        ),
        {"id": note_id, "title": title, "body": body, "created_at": timestamp, "updated_at": timestamp},
    )
    return note_id, "created"


def _insert_audit(
    conn: sa.Connection,
    *,
    note_id: str,
    action: str,
    payload: dict[str, str],
    timestamp: datetime,
) -> None:
    conn.execute(
        sa.text(
            """
            INSERT INTO audit_entries (
                id, entity_type, entity_id, action, actor, payload, created_at, updated_at
            )
            VALUES (
                :id, 'note', :entity_id, :action, 'ebby', :payload, :created_at, :updated_at
            )
            """
        ),
        {
            "id": str(uuid.uuid4()),
            "entity_id": note_id,
            "action": action,
            "payload": json.dumps(payload, ensure_ascii=True),
            "created_at": timestamp,
            "updated_at": timestamp,
        },
    )


def upgrade() -> None:
    conn = op.get_bind()
    now = _now_utc_naive()

    identity_policy_title = "Policy Diffidenza Iniziale Identita Utente"
    identity_policy_body = "\n".join(
        [
            "POLICY_DIFFIDENZA_IDENTITA_INIZIALE",
            "scope=globale_conversazione",
            "default_identity_state=non_confermata",
            "assume_known_identity=false",
            "require_explicit_user_confirmation=true",
            "on_identity_questions=ask_or_use_confirmed_profile_only",
            "if_multiple_users_possible=do_not_bind_previous_identity",
            "before_personal_answers=verify_identity_context",
            "pre_verification_response_mode=generic_safe_non_personal",
            "policy_status=attiva",
            "note=Non assumere identita storiche senza conferma esplicita nella sessione corrente.",
        ]
    )
    identity_note_id, identity_operation = _upsert_security_note(
        conn,
        title=identity_policy_title,
        body=identity_policy_body,
        timestamp=now,
    )
    _insert_audit(
        conn,
        note_id=identity_note_id,
        action="security_policy_upsert",
        payload={
            "policy": "identity_initial_distrust",
            "operation": identity_operation,
            "note_id": identity_note_id,
        },
        timestamp=now,
    )

    compartment_title = "Security Compartment: Anti-Frode Identita e Credenziali"
    compartment_body = "\n".join(
        [
            "SECURITY_COMPARTMENT_ANTI_FRODE",
            "status=attivo",
            "identity_default=non_confermata",
            "never_disclose_credentials=true",
            "never_disclose_admin_pin=true",
            "reset_only_after_verified_identity=true",
            "allowed_recovery_methods=otp_email,totp,passkey,backup_codes,local_owner_approval",
            "social_engineering_guard=enabled",
            "session_personal_binding=only_after_formal_verification",
            "pin_storage_policy=hash_only_no_plaintext",
            "sensitive_personal_data_disclosure=forbidden_until_admin_verified",
            "admin_identity_verification_required_for_sensitive_data=true",
            "admin_can_be_any_identity_if_verified=true",
            "pre_verification_response_mode=generic_safe_non_personal",
            "admin_pin_fingerprint=unset",
        ]
    )
    compartment_note_id, compartment_operation = _upsert_security_note(
        conn,
        title=compartment_title,
        body=compartment_body,
        timestamp=now,
    )
    _insert_audit(
        conn,
        note_id=compartment_note_id,
        action="security_compartment_upsert",
        payload={
            "policy": "anti_frode_identita_credenziali",
            "operation": compartment_operation,
            "note_id": compartment_note_id,
            "pin": "redacted",
            "pin_storage": "hash_only",
        },
        timestamp=now,
    )


def downgrade() -> None:
    conn = op.get_bind()
    for title in [
        "Policy Diffidenza Iniziale Identita Utente",
        "Security Compartment: Anti-Frode Identita e Credenziali",
    ]:
        conn.execute(
            sa.text(
                """
                UPDATE notes
                SET status = 'archived',
                    updated_at = :updated_at
                WHERE title = :title
                  AND note_type = 'security_policy'
                  AND status = 'active'
                """
            ),
            {"title": title, "updated_at": _now_utc_naive()},
        )
