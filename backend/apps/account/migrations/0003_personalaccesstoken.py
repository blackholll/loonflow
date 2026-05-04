# Generated manually for personal access tokens

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_user_external_user_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonalAccessToken",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("label", models.JSONField(blank=True, default=dict, verbose_name="label")),
                ("creator_id", models.UUIDField(default=uuid.uuid4, editable=False, null=True, verbose_name="creator_id")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="created_at")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="updated_at")),
                (
                    "tenant_id",
                    models.UUIDField(default="00000000-0000-0000-0000-000000000001", verbose_name="tenant_id"),
                ),
                ("token_label", models.CharField(blank=True, default="", max_length=200, verbose_name="token_label")),
                ("secret_ciphertext", models.TextField(blank=True, default="", verbose_name="secret_ciphertext")),
                ("mask_prefix", models.CharField(blank=True, default="", max_length=64, verbose_name="mask_prefix")),
                ("expires_at", models.DateTimeField(blank=True, null=True, verbose_name="expires_at")),
                ("last_used_at", models.DateTimeField(blank=True, null=True, verbose_name="last_used_at")),
                ("revoked_at", models.DateTimeField(blank=True, null=True, verbose_name="revoked_at")),
                (
                    "user",
                    models.ForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="personal_access_tokens",
                        to=settings.AUTH_USER_MODEL,
                        to_field="id",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
