# Generated by Django 2.2 on 2020-05-26 21:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Devtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Framework',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ide_stack', models.CharField(choices=[('node-js', 'NodeJS'), ('python', 'Python'), ('android', 'Android'), ('angular', 'Angular'), ('php', 'PHP')], default='node-js', max_length=140)),
                ('name', models.CharField(max_length=140)),
                ('image', models.CharField(blank=True, max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Projecttype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=140, null=True)),
                ('brief', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=2000, null=True)),
                ('level', models.CharField(blank=True, max_length=200, null=True)),
                ('concept', models.CharField(blank=True, max_length=200, null=True)),
                ('tags', models.CharField(blank=True, max_length=900, null=True)),
                ('projectimage1', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage2', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage3', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage4', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage5', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage6', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage7', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage8', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage9', models.CharField(blank=True, max_length=500, null=True)),
                ('projectimage10', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement1', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement2', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement3', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement4', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement5', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement6', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement7', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement8', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement9', models.CharField(blank=True, max_length=500, null=True)),
                ('requirement10', models.CharField(blank=True, max_length=500, null=True)),
                ('hasvideo', models.BooleanField(default=False)),
                ('duration', models.DurationField(default=datetime.timedelta(0, 7200))),
                ('project_template', models.URLField(blank=True, null=True)),
                ('devtype', models.ForeignKey(null=True, on_delete=False, to='projects.Devtype')),
                ('framework', models.ForeignKey(null=True, on_delete=False, to='projects.Framework')),
                ('owner', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
                ('projecttype', models.ForeignKey(null=True, on_delete=False, to='projects.Projecttype')),
            ],
        ),
        migrations.CreateModel(
            name='level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Language')),
            ],
        ),
        migrations.AddField(
            model_name='framework',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='projects.Language'),
        ),
    ]
