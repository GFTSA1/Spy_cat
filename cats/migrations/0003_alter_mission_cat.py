# Generated by Django 5.1.3 on 2024-11-30 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0002_rename_complete_state_mission_is_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='cat',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cats.cat'),
        ),
    ]
