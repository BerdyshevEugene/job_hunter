# Generated by Django 3.2 on 2022-09-16 13:16

from django.db import migrations, models
import django.db.models.deletion
import find_jobs.models


class Migration(migrations.Migration):

    dependencies = [
        ('find_jobs', '0003_alter_error_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_data', models.JSONField(default=find_jobs.models.default_urls)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find_jobs.city', verbose_name='city')),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find_jobs.specialization', verbose_name='specialization')),
            ],
            options={
                'unique_together': {('city', 'specialization')},
            },
        ),
    ]
