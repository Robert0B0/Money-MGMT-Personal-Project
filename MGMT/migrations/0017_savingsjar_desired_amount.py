# Generated by Django 3.1.1 on 2020-10-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0016_auto_20201017_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsjar',
            name='Desired_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]