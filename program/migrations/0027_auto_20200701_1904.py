# Generated by Django 2.2.4 on 2020-07-01 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0026_auto_20200701_1825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='becomedistributor',
            name='daily_sales_qty',
        ),
        migrations.RemoveField(
            model_name='becomedistributor',
            name='demand_level',
        ),
        migrations.AlterField(
            model_name='becomedistributor',
            name='weekly_sales_qty',
            field=models.IntegerField(default=2, null=True),
        ),
    ]
