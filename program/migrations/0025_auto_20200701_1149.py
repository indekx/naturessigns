# Generated by Django 2.2.4 on 2020-07-01 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0024_auto_20200701_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='becomedistributor',
            name='media_type',
            field=models.ManyToManyField(related_name='seleted_media_types', to='program.MediaType', verbose_name='seleted media types'),
        ),
    ]
