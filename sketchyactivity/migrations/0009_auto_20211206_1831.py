# Generated by Django 3.2.9 on 2021-12-06 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sketchyactivity', '0008_auto_20211204_0408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metastuff',
            name='sale_end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='metastuff',
            name='sale_start',
            field=models.DateField(),
        ),
    ]