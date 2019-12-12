# Generated by Django 2.2.4 on 2019-11-13 17:33

from django.db import migrations, models
import documents.utils


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_auto_20191112_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents', validators=[documents.utils.validate_file_size]),
        ),
    ]