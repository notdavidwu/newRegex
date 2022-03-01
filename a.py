# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Analysetext(models.Model):
    orderno = models.IntegerField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    reporttext = models.CharField(db_column='ReportText', max_length=4000)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AnalyseText'


class Examlist(models.Model):
    visitno = models.IntegerField(db_column='VisitNo', blank=True, null=True)  # Field name made lowercase.
    chartno = models.IntegerField(db_column='ChartNo', blank=True, null=True)  # Field name made lowercase.
    medtype = models.CharField(db_column='MedType', max_length=4, blank=True, null=True)  # Field name made lowercase.
    exectime = models.DateField(db_column='ExecTime', blank=True, null=True)  # Field name made lowercase.
    orderno = models.IntegerField(db_column='OrderNo', blank=True, null=True)  # Field name made lowercase.
    reporttime = models.DateField(db_column='ReportTime', blank=True, null=True)  # Field name made lowercase.
    reporttext = models.TextField(db_column='ReportText', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExamList'


class Localization(models.Model):
    id = models.CharField(max_length=50, blank=True, null=True)
    pid = models.CharField(db_column='PID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sid = models.CharField(db_column='SID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    sen = models.CharField(db_column='SEN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    suv = models.CharField(db_column='SUV', max_length=50, blank=True, null=True)  # Field name made lowercase.
    x = models.CharField(max_length=50, blank=True, null=True)
    y = models.CharField(max_length=50, blank=True, null=True)
    z = models.CharField(max_length=50, blank=True, null=True)
    labelgroup = models.CharField(db_column='LabelGroup', max_length=50, blank=True, null=True)  # Field name made lowercase.
    labelname = models.CharField(db_column='LabelName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    labelrecord = models.CharField(db_column='LabelRecord', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Localization'


class Medtypeset(models.Model):
    medtype = models.CharField(db_column='MedType', primary_key=True, max_length=4)  # Field name made lowercase.
    item = models.CharField(db_column='Item', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MedTypeSet'


class Patientexam(models.Model):
    id = models.IntegerField(db_column='ID', blank=True, null=True)  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', primary_key=True)  # Field name made lowercase.
    orderno = models.IntegerField(db_column='OrderNo')  # Field name made lowercase.
    icdcode = models.CharField(db_column='IcdCode', max_length=8)  # Field name made lowercase.
    diagdate = models.DateField(db_column='DiagDate', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=20, blank=True, null=True)  # Field name made lowercase.
    medordertime = models.DateField(db_column='MedOrderTime', blank=True, null=True)  # Field name made lowercase.
    medexectime = models.DateField(db_column='MedExecTime', blank=True, null=True)  # Field name made lowercase.
    medsummary = models.TextField(db_column='MedSummary', blank=True, null=True)  # Field name made lowercase.
    medtype = models.CharField(db_column='MedType', max_length=4, blank=True, null=True)  # Field name made lowercase.
    adopted = models.CharField(db_column='Adopted', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PatientExam'
        unique_together = (('pid', 'orderno', 'icdcode'),)


class Patientlist(models.Model):
    id = models.AutoField(db_column='ID')  # Field name made lowercase.
    pid = models.IntegerField(db_column='PID', primary_key=True)  # Field name made lowercase.
    orderno = models.IntegerField(db_column='OrderNo')  # Field name made lowercase.
    icdcode = models.CharField(db_column='IcdCode', max_length=8)  # Field name made lowercase.
    diagdate = models.DateField(db_column='DiagDate', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='Source', max_length=20, blank=True, null=True)  # Field name made lowercase.
    medordertime = models.DateField(db_column='MedOrderTime', blank=True, null=True)  # Field name made lowercase.
    medexectime = models.DateField(db_column='MedExecTime', blank=True, null=True)  # Field name made lowercase.
    medoperdate = models.DateField(db_column='MedOperDate')  # Field name made lowercase.
    medsummary = models.TextField(db_column='MedSummary', blank=True, null=True)  # Field name made lowercase.
    medtype = models.CharField(db_column='MedType', max_length=4)  # Field name made lowercase.
    adopted = models.CharField(db_column='Adopted', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PatientList'
        unique_together = (('pid', 'orderno', 'icdcode', 'medoperdate', 'medtype'),)


class Researchsubject(models.Model):
    subjectid = models.AutoField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    subjectname = models.CharField(db_column='SubjectName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    enrolledstartdate = models.DateField(db_column='EnrolledStartDate', blank=True, null=True)  # Field name made lowercase.
    enrolledenddate = models.DateField(db_column='EnrolledEndDate', blank=True, null=True)  # Field name made lowercase.
    forwarddays = models.IntegerField(db_column='ForwardDays', blank=True, null=True)  # Field name made lowercase.
    backworddays = models.IntegerField(db_column='BackwordDays', blank=True, null=True)  # Field name made lowercase.
    irb = models.CharField(db_column='IRB', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ResearchSubject'


class Subjectenrolleddiagnosis(models.Model):
    subjectid = models.IntegerField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    icdcode = models.CharField(db_column='ICDCode', max_length=8)  # Field name made lowercase.
    codever = models.SmallIntegerField(db_column='CodeVer', blank=True, null=True)  # Field name made lowercase.
    topography = models.CharField(db_column='Topography', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubjectEnrolledDiagnosis'
        unique_together = (('subjectid', 'icdcode'),)


class Subjectenrolledmedtype(models.Model):
    subjectid = models.IntegerField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    medtype = models.SmallIntegerField(db_column='MedType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubjectEnrolledMedType'
        unique_together = (('subjectid', 'medtype'),)


class Subjectlabelcontent(models.Model):
    labelgroupid = models.IntegerField(db_column='LabelGroupID', primary_key=True)  # Field name made lowercase.
    seqno = models.SmallIntegerField(db_column='SeqNo')  # Field name made lowercase.
    labelname = models.CharField(db_column='LabelName', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubjectLabelContent'
        unique_together = (('labelgroupid', 'seqno'),)


class Subjectlabelgroup(models.Model):
    labelgroupid = models.AutoField(db_column='LabelGroupID')  # Field name made lowercase.
    subjectid = models.IntegerField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    seqno = models.SmallIntegerField(db_column='SeqNo')  # Field name made lowercase.
    labelgroup = models.CharField(db_column='LabelGroup', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubjectLabelGroup'
        unique_together = (('subjectid', 'seqno'),)


class Subjectpatientlist(models.Model):
    subjectid = models.IntegerField(db_column='SubjectID', primary_key=True)  # Field name made lowercase.
    patientlistid = models.IntegerField(db_column='PatientListID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SubjectPatientList'
        unique_together = (('subjectid', 'patientlistid'),)


class Token(models.Model):
    token = models.CharField(db_column='Token', primary_key=True, max_length=200)  # Field name made lowercase.
    tokenid = models.AutoField(db_column='TokenID', unique=True)  # Field name made lowercase.
    tokentype = models.CharField(db_column='TokenType', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Token'


class UploadFilemodel(models.Model):
    title = models.CharField(max_length=50)
    file = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'Upload_filemodel'
