# Generated by Django 2.1.7 on 2019-09-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_project_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
