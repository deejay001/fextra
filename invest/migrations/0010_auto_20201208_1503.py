# Generated by Django 3.0.8 on 2020-12-08 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0009_auto_20201208_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referal',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invest.Profile', unique=True),
        ),
    ]