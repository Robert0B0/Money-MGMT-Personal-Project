# Generated by Django 3.1.1 on 2020-10-08 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MGMT', '0002_auto_20201008_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyactivity',
            name='category',
            field=models.CharField(choices=[('Outcome', (('expenses', 'Expenses'), ('upkeep', 'Upkeep'), ('unforeseen', 'Unforeseen'))), ('Income', (('monthly income', 'Monthly Income'), ('dividents', 'Dividents'), ('other', 'Other')))], default='Outcome', max_length=200),
        ),
    ]
