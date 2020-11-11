# Generated by Django 3.1.1 on 2020-11-10 00:06

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0030_auto_20201109_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growthinvestment',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.1000000000000000055511151231257827021181583404541015625')), django.core.validators.MaxValueValidator(Decimal('100'))]),
        ),
    ]
