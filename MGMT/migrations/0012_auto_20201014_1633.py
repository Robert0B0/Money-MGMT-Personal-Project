# Generated by Django 3.1.1 on 2020-10-14 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0011_auto_20201014_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyrecord',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
