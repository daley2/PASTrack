from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0019_case_draft_id_and_optional_tracking"),
    ]

    operations = [
        migrations.AlterField(
            model_name="casedocument",
            name="file",
            field=models.FileField(max_length=500, upload_to="core.models.case_document_upload_to"),
        ),
    ]
