# Generated by Django 3.2 on 2022-09-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_jobs', '0002_error'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='data',
            field=models.JSONField(),
        ),
    ]