from __future__ import annotations

import uuid

from django.db import migrations, models


def populate_case_draft_ids(apps, schema_editor):
    Case = apps.get_model("core", "Case")
    for c in Case.objects.filter(draft_id__isnull=True).only("id"):
        c.draft_id = uuid.uuid4()
        c.save(update_fields=["draft_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_case_case_type_case_client_email_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="case",
            name="draft_id",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name="case",
            name="tracking_id",
            field=models.CharField(blank=True, editable=False, max_length=30, null=True, unique=True),
        ),
        migrations.RunPython(populate_case_draft_ids, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="case",
            name="draft_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
