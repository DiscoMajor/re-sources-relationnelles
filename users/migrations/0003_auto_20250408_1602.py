# Generated by Django 3.2 on 2025-04-08 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20250408_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='citoyen',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='moderator',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='superadmin',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='citoyen',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='moderator',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='superadmin',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
