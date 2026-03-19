from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_case_client_contact_alter_case_client_name'),
    ]

    def _forwards(apps, schema_editor):
        if schema_editor.connection.vendor != "postgresql":
            return
        schema_editor.execute("ALTER TABLE core_case DROP COLUMN IF EXISTS last_password_change_at;")
        schema_editor.execute("ALTER TABLE core_case DROP COLUMN IF EXISTS password_change_count_this_month;")
        schema_editor.execute("ALTER TABLE core_case DROP COLUMN IF EXISTS password_reset_code;")
        schema_editor.execute("ALTER TABLE core_case DROP COLUMN IF EXISTS password_reset_code_created_at;")

    def _backwards(apps, schema_editor):
        if schema_editor.connection.vendor != "postgresql":
            return
        schema_editor.execute("ALTER TABLE core_case ADD COLUMN last_password_change_at timestamp with time zone NULL;")
        schema_editor.execute("ALTER TABLE core_case ADD COLUMN password_change_count_this_month smallint DEFAULT 0 NOT NULL;")
        schema_editor.execute("ALTER TABLE core_case ADD COLUMN password_reset_code varchar(6) DEFAULT '' NOT NULL;")
        schema_editor.execute("ALTER TABLE core_case ADD COLUMN password_reset_code_created_at timestamp with time zone NULL;")

    operations = [
        migrations.RunPython(_forwards, _backwards),
    ]
