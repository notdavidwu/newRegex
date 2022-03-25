# Generated by Django 3.2.10 on 2022-03-25 00:07

import Upload.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to=Upload.models.user_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicalRecordNumber', models.CharField(max_length=1000, null=True)),
                ('dicom_date', models.CharField(max_length=1000, null=True)),
                ('seriesNumber', models.CharField(max_length=1000, null=True)),
                ('username', models.CharField(max_length=1000, null=True)),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('path', models.CharField(max_length=1000, null=True)),
            ],
        ),
    ]
