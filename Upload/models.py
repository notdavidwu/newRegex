from django.db import models


# Create your models here.
class upload(models.Model):
    medicalRecordNumber = models.CharField(max_length=1000,null=True)
    dicom_date = models.CharField(max_length=1000,null=True)  # DICOM_date
    seriesNumber = models.CharField(max_length=1000,null=True)  # DICOM_date
    username = models.CharField(max_length=1000,null=True)
    upload_date = models.DateTimeField(auto_now=True)
    path = models.CharField(max_length=1000,null=True)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/%Y%m%d-{0}'.format(filename)


class FileModel(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path)
