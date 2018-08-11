# Generated by Django 2.0.7 on 2018-08-11 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thinking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('picture', models.ImageField(blank=True, upload_to='thinking')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.Item')),
            ],
        ),
    ]