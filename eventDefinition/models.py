# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Examreporttext(models.Model):
    orderNo = models.IntegerField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    reportTime = models.DateTimeField(db_column='reportTime')  # Field name made lowercase.
    reportDiag = models.CharField(db_column='reportDiag', max_length=1500, db_collation='Chinese_Taiwan_Stroke_CS_AS')  # Field name made lowercase.
    reportText = models.TextField(db_column='reportText', db_collation='Chinese_Taiwan_Stroke_CS_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'examReportText'


class Medorder(models.Model):
    visitNo = models.IntegerField(db_column='VisitNo')  # Field name made lowercase.
    orderNo = models.IntegerField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    execTime = models.DateTimeField(db_column='execTime', blank=True, null=True)  # Field name made lowercase.
    visitZone = models.CharField(db_column='visitZone', max_length=1, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)  # Field name made lowercase.
    visitGroup = models.IntegerField(db_column='visitGroup', blank=True, null=True)  # Field name made lowercase.
    source = models.IntegerField()
    medtype = models.SmallIntegerField(db_column='medType')  # Field name made lowercase.
    trancode = models.CharField(db_column='tranCode', max_length=1, db_collation='Chinese_Taiwan_Stroke_CS_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medOrder'


class Medtypeset(models.Model):
    medtype = models.SmallIntegerField(db_column='medType', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='typeName', max_length=100, db_collation='Chinese_Taiwan_Stroke_CS_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vMedTypeSet'


class Patientinfo(models.Model):
    aicno = models.IntegerField(db_column='aicNo', primary_key=True, default=0)  # Field name made lowercase.
    birthday = models.DateTimeField(db_column='birthDay',null = True)  # Field name made lowercase.
    sex = models.CharField(max_length=1, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)
    def __str__(self):
        return str(self.aicno)

    class Meta:
        managed = False
        db_table = 'vPatientInfo'
        


class Visitrecord(models.Model):
    visitno = models.IntegerField(db_column='VisitNo')  # Field name made lowercase.
    aicno = models.IntegerField(db_column='aicNo', primary_key=True, default=0)  # Field name made lowercase.
    visitdate = models.DateTimeField(db_column='visitDate')  # Field name made lowercase.
    visitzone = models.CharField(db_column='visitZone', max_length=1, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)  # Field name made lowercase.
    visittype = models.CharField(db_column='visitType', max_length=2, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)  # Field name made lowercase.
    visitseqno = models.CharField(db_column='visitSeqNo', max_length=4, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)  # Field name made lowercase.
    sourcetype = models.SmallIntegerField(db_column='sourceType', blank=True, null=True)  # Field name made lowercase.
    sourceno = models.SmallIntegerField(db_column='sourceNo', blank=True, null=True)  # Field name made lowercase.
    divno = models.SmallIntegerField(db_column='divNo', blank=True, null=True)  # Field name made lowercase.
    visitstatus = models.CharField(db_column='visitStatus', max_length=1, db_collation='Chinese_Taiwan_Stroke_CS_AS', blank=True, null=True)  # Field name made lowercase.
    outdate = models.DateTimeField(db_column='outDate', blank=True, null=True)  # Field name made lowercase.
    outtype = models.SmallIntegerField(db_column='outType', blank=True, null=True)  # Field name made lowercase.
    def __str__(self):
        return str(self.aicno)
    class Meta:
        managed = True
        db_table = 'fVisitRecord'
        # unique_together = (('aicno', 'visitno'),)
