# Generated by Django 5.1.7 on 2025-03-29 22:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_remove_chatroom_name'),
        ('move_on', '0004_category_ticket_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendants', to='move_on.team')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendant_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'attendants',
            },
        ),
        migrations.CreateModel(
            name='ChatQueue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ticket', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat_queue', to='move_on.ticket')),
            ],
            options={
                'db_table': 'chat_queue',
            },
        ),
        migrations.CreateModel(
            name='ChatSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto_assign', models.BooleanField(default=True)),
                ('balance_tickets', models.BooleanField(default=True)),
                ('max_tickets_per_attendant', models.IntegerField(default=5)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat_settings', to='move_on.profile')),
            ],
            options={
                'db_table': 'chat_settings',
            },
        ),
    ]
