# Generated by Django 4.2.10 on 2024-02-18 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_topis_room_topics'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='topics',
            new_name='topic',
        ),
    ]