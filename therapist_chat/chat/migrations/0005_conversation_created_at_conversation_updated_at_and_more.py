# Generated by Django 5.0.6 on 2024-07-13 22:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_userprofile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversation',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='status',
            field=models.IntegerField(choices=[(1, 'active'), (2, 'requested'), (3, 'inprogress'), (4, 'closed')], default=4),
        ),
    ]
