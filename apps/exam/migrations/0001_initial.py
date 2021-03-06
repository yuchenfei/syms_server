# Generated by Django 2.0.7 on 2018-08-11 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('a', models.CharField(blank=True, max_length=50)),
                ('b', models.CharField(blank=True, max_length=50)),
                ('c', models.CharField(blank=True, max_length=50)),
                ('d', models.CharField(blank=True, max_length=50)),
                ('answer', models.CharField(max_length=1)),
            ],
        ),
    ]
