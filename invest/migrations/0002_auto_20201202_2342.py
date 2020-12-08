# Generated by Django 3.0.8 on 2020-12-02 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='output',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='stake',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
