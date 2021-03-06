# Generated by Django 2.0.7 on 2018-08-23 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20180818_1656'),
        ('exam', '0004_examsetting_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.ExamSetting')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Student')),
            ],
        ),
    ]
