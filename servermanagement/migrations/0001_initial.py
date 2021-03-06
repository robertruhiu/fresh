# Generated by Django 2.2 on 2020-05-26 21:45

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IdeFactory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stack', models.CharField(choices=[('node-js', 'NodeJS'), ('python', 'Python'), ('android', 'Android'), ('angular', 'Angular'), ('php', 'PHP')], default='node-js', max_length=140)),
                ('workspace_config', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, unique=True)),
                ('is_free', models.BooleanField(default=True)),
                ('ip_address', models.CharField(blank=True, max_length=140)),
                ('machine_id', models.CharField(blank=True, max_length=140)),
                ('setup_code', models.CharField(blank=True, max_length=140, unique=True)),
                ('decommissioned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ServerConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('snapshot_image', models.CharField(blank=True, max_length=140)),
                ('region', models.CharField(blank=True, max_length=140)),
                ('size_slug', models.CharField(blank=True, max_length=140)),
                ('type', models.CharField(choices=[('ide_server_config', 'IDE server config')], default='ide_server_config', max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('create_server', 'Create server'), ('create_workspace', 'Create Workspace'), ('send_mail', 'Send Mail'), ('monitor_workspace', 'Monitor Workspace'), ('start_analysis', 'Start Analysis'), ('transfer_files', 'Transfer Files'), ('get_analysis', 'Get Analysis'), ('clean_up', 'Clean Up')], default='create_server', max_length=140, null=True)),
                ('has_executed', models.BooleanField(default=False)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('setup_code', models.UUIDField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Assessment')),
            ],
        ),
        migrations.CreateModel(
            name='CandidateSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=140)),
                ('setup_code', models.CharField(blank=True, max_length=140, unique=True)),
                ('candidate_id', models.CharField(blank=True, max_length=140)),
                ('workspace_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('workspace_url', models.URLField(blank=True)),
                ('report', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('server_created', models.BooleanField(default=False)),
                ('domain_created', models.BooleanField(default=False)),
                ('workspace_created', models.BooleanField(default=False)),
                ('candidate_notified', models.BooleanField(default=False)),
                ('project_completed', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('formatted_report', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='frontend.Assessment')),
            ],
        ),
    ]
