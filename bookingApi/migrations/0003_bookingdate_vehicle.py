# Generated by Django 3.2.6 on 2021-08-04 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingApi', '0002_bookingdate_bookingprice_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdate',
            name='vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_name', to='bookingApi.vehicle'),
            preserve_default=False,
        ),
    ]