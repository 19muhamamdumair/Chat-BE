# Generated by Django 5.0.6 on 2024-07-13 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('therapist', 'Therapist'), ('parent', 'Parent')], max_length=20),
        ),
    ]
