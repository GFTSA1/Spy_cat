# Generated by Django 5.1.3 on 2024-11-30 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0003_alter_mission_cat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='target',
        ),
        migrations.AddField(
            model_name='mission',
            name='targets',
            field=models.ManyToManyField(to='cats.target'),
        ),
    ]
