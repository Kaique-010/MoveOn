# Generated by Django 5.1.7 on 2025-03-26 23:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('move_on', '0002_remove_ticketstatus_color_alter_ticket_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='move_on.profile'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_tickets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='move_on.ticketstatus'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Título'),
        ),
    ]
