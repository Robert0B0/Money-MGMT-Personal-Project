# Generated by Django 3.1.1 on 2020-10-17 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0014_remove_moneygoals_calculated_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile-default.png', null=True, upload_to=''),
        ),
    ]