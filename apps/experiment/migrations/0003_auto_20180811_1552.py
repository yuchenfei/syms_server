# Generated by Django 2.0.7 on 2018-08-11 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
        ('experiment', '0002_auto_20180811_1246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.IntegerField()),
                ('comment', models.CharField(max_length=255)),
                ('experiment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.Experiment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Student')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='grade',
            unique_together={('experiment', 'student')},
        ),
    ]
