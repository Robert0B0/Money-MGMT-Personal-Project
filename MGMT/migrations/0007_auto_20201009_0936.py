# Generated by Django 3.1.1 on 2020-10-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0006_auto_20201008_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneygoals',
            name='due_date',
            field=models.DateTimeField(null=True),
        ),
    ]
