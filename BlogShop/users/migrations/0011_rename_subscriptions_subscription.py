# Generated by Django 5.2.3 on 2025-07-10 22:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_profile_id_alter_profile_user_subscriptions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subscriptions',
            new_name='Subscription',
        ),
    ]
