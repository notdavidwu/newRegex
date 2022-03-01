# Generated by Django 2.2.24 on 2021-10-08 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DICOM', '0005_auto_20211004_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localization',
            old_name='IDN',
            new_name='LabelGroup',
        ),
        migrations.RenameField(
            model_name='localization',
            old_name='sno',
            new_name='LabelName',
        ),
        migrations.RenameField(
            model_name='localization',
            old_name='tumor',
            new_name='PID',
        ),
        migrations.AddField(
            model_name='localization',
            name='LabelRecord',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='localization',
            name='SEN',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='localization',
            name='SID',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
