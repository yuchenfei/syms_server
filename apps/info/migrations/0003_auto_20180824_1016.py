# Generated by Django 2.0.7 on 2018-08-24 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20180818_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('name', 'classes')},
        ),
    ]
