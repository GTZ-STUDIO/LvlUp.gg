# Generated by Django 5.0.2 on 2024-02-22 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_client_username_alter_client_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
