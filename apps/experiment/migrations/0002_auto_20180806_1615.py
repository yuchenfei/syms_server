# Generated by Django 2.0.7 on 2018-08-06 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='describe',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='remark',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
