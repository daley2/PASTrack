# Generated manually to fix IntegrityError in core_case

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_alter_case_client_contact_alter_case_client_name'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE core_case DROP COLUMN IF EXISTS last_password_change_at;
                ALTER TABLE core_case DROP COLUMN IF EXISTS password_change_count_this_month;
                ALTER TABLE core_case DROP COLUMN IF EXISTS password_reset_code;
                ALTER TABLE core_case DROP COLUMN IF EXISTS password_reset_code_created_at;
            """,
            reverse_sql="""
                ALTER TABLE core_case ADD COLUMN last_password_change_at timestamp with time zone NULL;
                ALTER TABLE core_case ADD COLUMN password_change_count_this_month smallint DEFAULT 0 NOT NULL;
                ALTER TABLE core_case ADD COLUMN password_reset_code varchar(6) DEFAULT '' NOT NULL;
                ALTER TABLE core_case ADD COLUMN password_reset_code_created_at timestamp with time zone NULL;
            """
        ),
    ]
