# Generated by Django 2.1.7 on 2019-09-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_task_muc_do_hoan_thanh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='IDproject',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
