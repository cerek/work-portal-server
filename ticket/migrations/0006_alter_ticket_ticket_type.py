# Generated by Django 3.2.20 on 2024-02-02 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_ticket_ticket_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='ticket.tickettype'),
        ),
    ]