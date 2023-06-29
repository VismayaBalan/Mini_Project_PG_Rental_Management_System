# Generated by Django 4.2.2 on 2023-06-29 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_pglist_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pglist',
            name='booked_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='login.customer'),
        ),
        migrations.AddField(
            model_name='pglist',
            name='booking_status',
            field=models.CharField(choices=[('Booked', 'Booked'), ('Not Booked', 'Not Booked')], default='Not Booked', max_length=10),
        ),
    ]
