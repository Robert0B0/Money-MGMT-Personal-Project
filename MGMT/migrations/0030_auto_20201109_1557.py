# Generated by Django 3.1.1 on 2020-11-09 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0029_auto_20201109_1555'),
    ]

    operations = [
        migrations.RenameField(
            model_name='growthinvestment',
            old_name='amount',
            new_name='current_amount',
        ),
        migrations.RenameField(
            model_name='growthinvestment',
            old_name='set_contribution',
            new_name='monthly_contribution',
        ),
    ]