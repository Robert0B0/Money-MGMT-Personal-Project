# Generated by Django 3.1.1 on 2020-10-17 19:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MGMT', '0015_auto_20201016_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyuser',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='savingsJar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naming', models.CharField(blank=True, default='Record', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MGMT.moneyuser')),
            ],
        ),
    ]