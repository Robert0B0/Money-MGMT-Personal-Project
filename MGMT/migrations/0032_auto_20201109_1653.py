# Generated by Django 3.1.1 on 2020-11-10 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0031_auto_20201109_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='growthinvestment',
            name='time_length',
            field=models.IntegerField(default=10),
        ),
    ]