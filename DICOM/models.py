from django.db import models

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
class Localization(models.Model):
    app_label = 'AICH'
    id = models.CharField(max_length=50, blank=True, primary_key=True)
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



class Drugset(models.Model):
    app_label = 'AIC8'
    drugno = models.AutoField(db_column='DrugNo',primary_key=True)  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', max_length=8)  # Field name made lowercase.
    zone = models.CharField(db_column='Zone', max_length=1)  # Field name made lowercase.
    itemname = models.CharField(db_column='ItemName', max_length=60)  # Field name made lowercase.
    pureitemname = models.CharField(db_column='PureItemName', max_length=60)  # Field name made lowercase.
    chinesename = models.CharField(db_column='ChineseName', max_length=30)  # Field name made lowercase.
    genericcode = models.CharField(db_column='GenericCode', max_length=9)  # Field name made lowercase.
    genericname = models.CharField(db_column='GenericName', max_length=100)  # Field name made lowercase.
    nhicode = models.CharField(db_column='NhiCode', max_length=12)  # Field name made lowercase.
    ahfscode = models.CharField(db_column='AhfsCode', max_length=10)  # Field name made lowercase.
    atc7code = models.CharField(db_column='Atc7Code', max_length=7)  # Field name made lowercase.
    atc7code2 = models.CharField(db_column='Atc7Code2', max_length=7)  # Field name made lowercase.
    atc7code3 = models.CharField(db_column='Atc7Code3', max_length=7)  # Field name made lowercase.
    atc7code4 = models.CharField(db_column='Atc7Code4', max_length=7)  # Field name made lowercase.
    atc7hintcode = models.CharField(db_column='Atc7HintCode', max_length=7)  # Field name made lowercase.
    atc7hintcode2 = models.CharField(db_column='Atc7HintCode2', max_length=7)  # Field name made lowercase.
    atc7hintcode3 = models.CharField(db_column='Atc7HintCode3', max_length=7)  # Field name made lowercase.
    atc7hintcode4 = models.CharField(db_column='Atc7HintCode4', max_length=7)  # Field name made lowercase.
    atc1 = models.CharField(db_column='Atc1', max_length=20)  # Field name made lowercase.
    atc2 = models.CharField(db_column='Atc2', max_length=40)  # Field name made lowercase.
    atc3 = models.CharField(db_column='Atc3', max_length=60)  # Field name made lowercase.
    nr = models.DecimalField(db_column='NR', max_digits=13, decimal_places=6)  # Field name made lowercase.
    ddd = models.DecimalField(db_column='DDD', max_digits=13, decimal_places=6)  # Field name made lowercase.
    opdstoragecode = models.CharField(db_column='OPDStorageCode', max_length=17)  # Field name made lowercase.
    inpstoragecode = models.CharField(db_column='INPStorageCode', max_length=10)  # Field name made lowercase.
    emgstoragecode = models.CharField(db_column='EMGStorageCode', max_length=10)  # Field name made lowercase.
    chemstoragecode = models.CharField(db_column='CHEMStorageCode', max_length=10)  # Field name made lowercase.
    barcode = models.CharField(db_column='BarCode', max_length=13)  # Field name made lowercase.
    represent = models.CharField(db_column='Represent', max_length=40)  # Field name made lowercase.
    manufactory = models.CharField(db_column='Manufactory', max_length=40)  # Field name made lowercase.
    licensenumber = models.CharField(db_column='LicenseNumber', max_length=10)  # Field name made lowercase.
    nhiprice = models.DecimalField(db_column='NhiPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    genprice = models.DecimalField(db_column='GenPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    salenhiprice = models.DecimalField(db_column='SaleNhiPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    salegenprice = models.DecimalField(db_column='SaleGenPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    form = models.SmallIntegerField(db_column='Form')  # Field name made lowercase.
    injection = models.CharField(db_column='Injection', max_length=500)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=500)  # Field name made lowercase.
    prescriptionprint = models.BooleanField(db_column='PrescriptionPrint')  # Field name made lowercase.
    storage = models.CharField(db_column='Storage', max_length=50)  # Field name made lowercase.
    indicationsa1 = models.CharField(db_column='IndicationsA1', max_length=50)  # Field name made lowercase.
    indicationsa2 = models.CharField(db_column='IndicationsA2', max_length=800)  # Field name made lowercase.
    nhinorm = models.TextField(db_column='NhiNorm')  # Field name made lowercase.
    nonnhi = models.CharField(db_column='NonNhi', max_length=50)  # Field name made lowercase.
    adultdosing = models.TextField(db_column='AdultDosing')  # Field name made lowercase.
    pediatricdosings = models.CharField(db_column='PediatricDosings', max_length=500)  # Field name made lowercase.
    adverseeffectsa1 = models.CharField(db_column='AdverseEffectsA1', max_length=50)  # Field name made lowercase.
    adverseeffectsa2 = models.CharField(db_column='AdverseEffectsA2', max_length=100)  # Field name made lowercase.
    contraindication = models.CharField(db_column='Contraindication', max_length=500)  # Field name made lowercase.
    precautions = models.CharField(db_column='Precautions', max_length=100)  # Field name made lowercase.
    breast = models.CharField(db_column='Breast', max_length=100)  # Field name made lowercase.
    childdosing = models.CharField(db_column='ChildDosing', max_length=200)  # Field name made lowercase.
    ctrldrug = models.CharField(db_column='CtrlDrug', max_length=1)  # Field name made lowercase.
    highalert = models.SmallIntegerField(db_column='HighAlert')  # Field name made lowercase.
    falldrug = models.SmallIntegerField(db_column='FallDrug')  # Field name made lowercase.
    isg6pd = models.BooleanField(db_column='IsG6PD')  # Field name made lowercase.
    isbioproduct = models.BooleanField(db_column='IsBioProduct')  # Field name made lowercase.
    isdoublecheck = models.BooleanField(db_column='IsDoubleCheck')  # Field name made lowercase.
    ischronic = models.BooleanField(db_column='IsChronic')  # Field name made lowercase.
    ispreexam = models.BooleanField(db_column='IsPreExam')  # Field name made lowercase.
    ispreexamaccept = models.BooleanField(db_column='IsPreExamAccept')  # Field name made lowercase.
    isspecialfree = models.BooleanField(db_column='IsSpecialFree')  # Field name made lowercase.
    isexpensive = models.BooleanField(db_column='IsExpensive')  # Field name made lowercase.
    isfreezer = models.BooleanField(db_column='IsFreezer')  # Field name made lowercase.
    ischemdrug = models.BooleanField(db_column='IsChemDrug')  # Field name made lowercase.
    isfalldrug = models.BooleanField(db_column='IsFallDrug')  # Field name made lowercase.
    isshowbag = models.BooleanField(db_column='IsShowBag')  # Field name made lowercase.
    isstataddcount = models.BooleanField(db_column='IsSTATAddCount')  # Field name made lowercase.
    pregnancy = models.CharField(db_column='Pregnancy', max_length=1)  # Field name made lowercase.
    pregnancydesc = models.CharField(db_column='PregnancyDesc', max_length=100)  # Field name made lowercase.
    trancode = models.SmallIntegerField(db_column='TranCode')  # Field name made lowercase.
    invcode = models.CharField(db_column='InvCode', max_length=8)  # Field name made lowercase.
    package = models.SmallIntegerField(db_column='Package')  # Field name made lowercase.
    packcapacity = models.DecimalField(db_column='PackCapacity', max_digits=7, decimal_places=2)  # Field name made lowercase.
    substitute = models.CharField(db_column='Substitute', max_length=8)  # Field name made lowercase.
    dividend = models.SmallIntegerField(db_column='Dividend')  # Field name made lowercase.
    saleunit = models.CharField(db_column='SaleUnit', max_length=4)  # Field name made lowercase.
    divisor = models.DecimalField(db_column='Divisor', max_digits=8, decimal_places=2)  # Field name made lowercase.
    doseunit = models.CharField(db_column='DoseUnit', max_length=4)  # Field name made lowercase.
    dosege = models.DecimalField(db_column='Dosege', max_digits=10, decimal_places=2)  # Field name made lowercase.
    dosegeunit = models.CharField(db_column='DosegeUnit', max_length=4)  # Field name made lowercase.
    volume = models.DecimalField(db_column='Volume', max_digits=5, decimal_places=1)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=4)  # Field name made lowercase.
    maxdaydoses = models.DecimalField(db_column='MaxDayDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maxorderdoses = models.DecimalField(db_column='MaxOrderDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    minorderdoses = models.DecimalField(db_column='MinOrderDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    squaredose = models.DecimalField(db_column='SquareDose', max_digits=6, decimal_places=1)  # Field name made lowercase.
    isintdose = models.BooleanField(db_column='IsIntDose')  # Field name made lowercase.
    days = models.SmallIntegerField(db_column='Days')  # Field name made lowercase.
    dose = models.DecimalField(db_column='Dose', max_digits=6, decimal_places=2)  # Field name made lowercase.
    usageno = models.SmallIntegerField(db_column='UsageNo')  # Field name made lowercase.
    wayno = models.SmallIntegerField(db_column='WayNo')  # Field name made lowercase.
    isself = models.BooleanField(db_column='IsSelf')  # Field name made lowercase.
    isaddcount = models.BooleanField(db_column='IsAddCount')  # Field name made lowercase.
    inpstatistics = models.SmallIntegerField(db_column='InpStatistics')  # Field name made lowercase.
    agedosing = models.CharField(db_column='AgeDosing', max_length=1)  # Field name made lowercase.
    organdosing = models.CharField(db_column='OrganDosing', max_length=1)  # Field name made lowercase.
    isdaily = models.BooleanField(db_column='IsDaily')  # Field name made lowercase.
    expirehour = models.SmallIntegerField(db_column='ExpireHour')  # Field name made lowercase.
    hasuserule = models.BooleanField(db_column='HasUseRule')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500)  # Field name made lowercase.
    nhistartdate = models.DateField(db_column='NhiStartDate')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DrugSet'


class Drugsetlog(models.Model):
    app_label = 'AIC8'
    itemcode = models.CharField(db_column='ItemCode', max_length=8)  # Field name made lowercase.
    zone = models.CharField(db_column='Zone', max_length=1)  # Field name made lowercase.
    itemname = models.CharField(db_column='ItemName', max_length=60)  # Field name made lowercase.
    pureitemname = models.CharField(db_column='PureItemName', max_length=60)  # Field name made lowercase.
    chinesename = models.CharField(db_column='ChineseName', max_length=30)  # Field name made lowercase.
    genericcode = models.CharField(db_column='GenericCode', max_length=9)  # Field name made lowercase.
    genericname = models.CharField(db_column='GenericName', max_length=100)  # Field name made lowercase.
    nhicode = models.CharField(db_column='NhiCode', max_length=12)  # Field name made lowercase.
    ahfscode = models.CharField(db_column='AhfsCode', max_length=10)  # Field name made lowercase.
    atc7code = models.CharField(db_column='Atc7Code', max_length=7)  # Field name made lowercase.
    atc7code2 = models.CharField(db_column='Atc7Code2', max_length=7)  # Field name made lowercase.
    atc7code3 = models.CharField(db_column='Atc7Code3', max_length=7)  # Field name made lowercase.
    atc7code4 = models.CharField(db_column='Atc7Code4', max_length=7)  # Field name made lowercase.
    atc7hintcode = models.CharField(db_column='Atc7HintCode', max_length=7)  # Field name made lowercase.
    atc7hintcode2 = models.CharField(db_column='Atc7HintCode2', max_length=7)  # Field name made lowercase.
    atc7hintcode3 = models.CharField(db_column='Atc7HintCode3', max_length=7)  # Field name made lowercase.
    atc7hintcode4 = models.CharField(db_column='Atc7HintCode4', max_length=7)  # Field name made lowercase.
    atc1 = models.CharField(db_column='Atc1', max_length=20)  # Field name made lowercase.
    atc2 = models.CharField(db_column='Atc2', max_length=40)  # Field name made lowercase.
    atc3 = models.CharField(db_column='Atc3', max_length=60)  # Field name made lowercase.
    nr = models.DecimalField(db_column='NR', max_digits=13, decimal_places=6)  # Field name made lowercase.
    ddd = models.DecimalField(db_column='DDD', max_digits=13, decimal_places=6)  # Field name made lowercase.
    opdstoragecode = models.CharField(db_column='OPDStorageCode', max_length=17)  # Field name made lowercase.
    inpstoragecode = models.CharField(db_column='INPStorageCode', max_length=10)  # Field name made lowercase.
    emgstoragecode = models.CharField(db_column='EMGStorageCode', max_length=10)  # Field name made lowercase.
    chemstoragecode = models.CharField(db_column='CHEMStorageCode', max_length=10)  # Field name made lowercase.
    barcode = models.CharField(db_column='BarCode', max_length=13)  # Field name made lowercase.
    represent = models.CharField(db_column='Represent', max_length=40)  # Field name made lowercase.
    manufactory = models.CharField(db_column='Manufactory', max_length=40)  # Field name made lowercase.
    licensenumber = models.CharField(db_column='LicenseNumber', max_length=10)  # Field name made lowercase.
    nhiprice = models.DecimalField(db_column='NhiPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    genprice = models.DecimalField(db_column='GenPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    salenhiprice = models.DecimalField(db_column='SaleNhiPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    salegenprice = models.DecimalField(db_column='SaleGenPrice', max_digits=11, decimal_places=4)  # Field name made lowercase.
    form = models.SmallIntegerField(db_column='Form')  # Field name made lowercase.
    injection = models.CharField(db_column='Injection', max_length=500)  # Field name made lowercase.
    dispose = models.CharField(db_column='Dispose', max_length=500)  # Field name made lowercase.
    prescriptionprint = models.BooleanField(db_column='PrescriptionPrint')  # Field name made lowercase.
    storage = models.CharField(db_column='Storage', max_length=50)  # Field name made lowercase.
    indicationsa1 = models.CharField(db_column='IndicationsA1', max_length=50)  # Field name made lowercase.
    indicationsa2 = models.CharField(db_column='IndicationsA2', max_length=800)  # Field name made lowercase.
    nhinorm = models.TextField(db_column='NhiNorm')  # Field name made lowercase.
    nonnhi = models.CharField(db_column='NonNhi', max_length=50)  # Field name made lowercase.
    adultdosing = models.CharField(db_column='AdultDosing', max_length=200)  # Field name made lowercase.
    pediatricdosings = models.CharField(db_column='PediatricDosings', max_length=500)  # Field name made lowercase.
    adverseeffectsa1 = models.CharField(db_column='AdverseEffectsA1', max_length=50)  # Field name made lowercase.
    adverseeffectsa2 = models.CharField(db_column='AdverseEffectsA2', max_length=100)  # Field name made lowercase.
    contraindication = models.CharField(db_column='Contraindication', max_length=500)  # Field name made lowercase.
    precautions = models.CharField(db_column='Precautions', max_length=100)  # Field name made lowercase.
    breast = models.CharField(db_column='Breast', max_length=100)  # Field name made lowercase.
    childdosing = models.CharField(db_column='ChildDosing', max_length=200)  # Field name made lowercase.
    ctrldrug = models.CharField(db_column='CtrlDrug', max_length=1)  # Field name made lowercase.
    highalert = models.SmallIntegerField(db_column='HighAlert')  # Field name made lowercase.
    falldrug = models.SmallIntegerField(db_column='FallDrug')  # Field name made lowercase.
    isg6pd = models.BooleanField(db_column='IsG6PD')  # Field name made lowercase.
    isbioproduct = models.BooleanField(db_column='IsBioProduct')  # Field name made lowercase.
    isdoublecheck = models.BooleanField(db_column='IsDoubleCheck')  # Field name made lowercase.
    ischronic = models.BooleanField(db_column='IsChronic')  # Field name made lowercase.
    ispreexam = models.BooleanField(db_column='IsPreExam')  # Field name made lowercase.
    ispreexamaccept = models.BooleanField(db_column='IsPreExamAccept')  # Field name made lowercase.
    isspecialfree = models.BooleanField(db_column='IsSpecialFree')  # Field name made lowercase.
    isexpensive = models.BooleanField(db_column='IsExpensive')  # Field name made lowercase.
    isfreezer = models.BooleanField(db_column='IsFreezer')  # Field name made lowercase.
    ischemdrug = models.BooleanField(db_column='IsChemDrug')  # Field name made lowercase.
    isfalldrug = models.BooleanField(db_column='IsFallDrug')  # Field name made lowercase.
    isshowbag = models.BooleanField(db_column='IsShowBag')  # Field name made lowercase.
    isstataddcount = models.BooleanField(db_column='IsSTATAddCount')  # Field name made lowercase.
    pregnancy = models.CharField(db_column='Pregnancy', max_length=1)  # Field name made lowercase.
    pregnancydesc = models.CharField(db_column='PregnancyDesc', max_length=100)  # Field name made lowercase.
    trancode = models.SmallIntegerField(db_column='TranCode')  # Field name made lowercase.
    invcode = models.CharField(db_column='InvCode', max_length=8)  # Field name made lowercase.
    package = models.SmallIntegerField(db_column='Package')  # Field name made lowercase.
    packcapacity = models.DecimalField(db_column='PackCapacity', max_digits=7, decimal_places=2)  # Field name made lowercase.
    substitute = models.CharField(db_column='Substitute', max_length=8)  # Field name made lowercase.
    dividend = models.SmallIntegerField(db_column='Dividend')  # Field name made lowercase.
    saleunit = models.CharField(db_column='SaleUnit', max_length=4)  # Field name made lowercase.
    divisor = models.DecimalField(db_column='Divisor', max_digits=8, decimal_places=2)  # Field name made lowercase.
    doseunit = models.CharField(db_column='DoseUnit', max_length=4)  # Field name made lowercase.
    dosege = models.DecimalField(db_column='Dosege', max_digits=10, decimal_places=2)  # Field name made lowercase.
    dosegeunit = models.CharField(db_column='DosegeUnit', max_length=4)  # Field name made lowercase.
    volume = models.DecimalField(db_column='Volume', max_digits=5, decimal_places=1)  # Field name made lowercase.
    unit = models.CharField(db_column='Unit', max_length=4)  # Field name made lowercase.
    maxdaydoses = models.DecimalField(db_column='MaxDayDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    maxorderdoses = models.DecimalField(db_column='MaxOrderDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    minorderdoses = models.DecimalField(db_column='MinOrderDoses', max_digits=10, decimal_places=2)  # Field name made lowercase.
    squaredose = models.DecimalField(db_column='SquareDose', max_digits=6, decimal_places=1)  # Field name made lowercase.
    isintdose = models.BooleanField(db_column='IsIntDose')  # Field name made lowercase.
    days = models.SmallIntegerField(db_column='Days')  # Field name made lowercase.
    dose = models.DecimalField(db_column='Dose', max_digits=6, decimal_places=2)  # Field name made lowercase.
    usageno = models.SmallIntegerField(db_column='UsageNo')  # Field name made lowercase.
    wayno = models.SmallIntegerField(db_column='WayNo')  # Field name made lowercase.
    isself = models.BooleanField(db_column='IsSelf')  # Field name made lowercase.
    isaddcount = models.BooleanField(db_column='IsAddCount')  # Field name made lowercase.
    inpstatistics = models.SmallIntegerField(db_column='InpStatistics')  # Field name made lowercase.
    agedosing = models.CharField(db_column='AgeDosing', max_length=1)  # Field name made lowercase.
    organdosing = models.CharField(db_column='OrganDosing', max_length=1)  # Field name made lowercase.
    isdaily = models.BooleanField(db_column='IsDaily')  # Field name made lowercase.
    expirehour = models.SmallIntegerField(db_column='ExpireHour')  # Field name made lowercase.
    hasuserule = models.BooleanField(db_column='HasUseRule')  # Field name made lowercase.
    remark = models.CharField(db_column='Remark', max_length=500)  # Field name made lowercase.
    nhistartdate = models.DateField(db_column='NhiStartDate')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DrugSetLog'
        unique_together = (('updatetime', 'itemcode', 'zone'),)


class Examreporttext(models.Model):
    app_label = 'AIC8'
    orderno = models.IntegerField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    reportno = models.CharField(db_column='ReportNo', max_length=30)  # Field name made lowercase.
    reporttype = models.SmallIntegerField(db_column='ReportType')  # Field name made lowercase.
    reportdiag = models.CharField(db_column='ReportDiag', max_length=1500)  # Field name made lowercase.
    modifycount = models.SmallIntegerField(db_column='ModifyCount')  # Field name made lowercase.
    reporttext = models.TextField(db_column='ReportText')  # Field name made lowercase.
    reportuser = models.SmallIntegerField(db_column='ReportUser')  # Field name made lowercase.
    reporttime = models.DateTimeField(db_column='ReportTime')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExamReportText'


class Meditem(models.Model):
    app_label = 'AIC8'
    itemno = models.AutoField(db_column='ItemNo', primary_key=True)  # Field name made lowercase.
    orderno = models.ForeignKey('Medorder', models.DO_NOTHING, db_column='OrderNo')  # Field name made lowercase.
    seqno = models.SmallIntegerField(db_column='SeqNo')  # Field name made lowercase.
    itemcode = models.CharField(db_column='ItemCode', max_length=8)  # Field name made lowercase.
    dose = models.DecimalField(db_column='Dose', max_digits=9, decimal_places=3)  # Field name made lowercase.
    squaredose = models.DecimalField(db_column='SquareDose', max_digits=9, decimal_places=3)  # Field name made lowercase.
    usageno = models.SmallIntegerField(db_column='UsageNo')  # Field name made lowercase.
    wayno = models.SmallIntegerField(db_column='WayNo', blank=True, null=True)  # Field name made lowercase.
    keeptime = models.SmallIntegerField(db_column='KeepTime', blank=True, null=True)  # Field name made lowercase.
    totqty = models.DecimalField(db_column='TotQty', max_digits=9, decimal_places=3)  # Field name made lowercase.
    execqty = models.DecimalField(db_column='ExecQty', max_digits=9, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    totcomposeqty = models.DecimalField(db_column='TotComposeQty', max_digits=9, decimal_places=3)  # Field name made lowercase.
    isself = models.BooleanField(db_column='IsSelf')  # Field name made lowercase.
    ismill = models.BooleanField(db_column='IsMill')  # Field name made lowercase.
    mark = models.CharField(db_column='Mark', max_length=1)  # Field name made lowercase.
    advise = models.CharField(db_column='Advise', max_length=100, blank=True, null=True)  # Field name made lowercase.
    linktype = models.CharField(db_column='LinkType', max_length=1, blank=True, null=True)  # Field name made lowercase.
    linkno = models.IntegerField(db_column='LinkNo', blank=True, null=True)  # Field name made lowercase.
    treatcheckuser = models.SmallIntegerField(db_column='TreatCheckUser', blank=True, null=True)  # Field name made lowercase.
    checkuser = models.SmallIntegerField(db_column='CheckUser', blank=True, null=True)  # Field name made lowercase.
    checktime = models.DateTimeField(db_column='CheckTime', blank=True, null=True)  # Field name made lowercase.
    checkstatus = models.SmallIntegerField(db_column='CheckStatus')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    treatuser = models.SmallIntegerField(db_column='TreatUser', blank=True, null=True)  # Field name made lowercase.
    treattime = models.DateTimeField(db_column='TreatTime', blank=True, null=True)  # Field name made lowercase.
    treatstatus = models.CharField(db_column='TreatStatus', max_length=1)  # Field name made lowercase.
    invno = models.IntegerField(db_column='InvNo')  # Field name made lowercase.
    invloc = models.SmallIntegerField(db_column='InvLoc')  # Field name made lowercase.
    preaccountdate = models.DateField(db_column='PreAccountDate')  # Field name made lowercase.
    ischarge = models.BooleanField(db_column='IsCharge')  # Field name made lowercase.
    chargeno = models.IntegerField(db_column='ChargeNo')  # Field name made lowercase.
    accountno = models.IntegerField(db_column='AccountNo')  # Field name made lowercase.
    timestamp = models.IntegerField(db_column='TimeStamp')  # Field name made lowercase.
    preendtime = models.DateTimeField(db_column='PreEndTime', blank=True, null=True)  # Field name made lowercase.
    docno = models.BigIntegerField(db_column='DocNo')  # Field name made lowercase.
    itemgroup = models.SmallIntegerField(db_column='ItemGroup')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MedItem'


class Medorder(models.Model):
    app_label = 'AIC8'
    orderno = models.AutoField(db_column='OrderNo', primary_key=True)  # Field name made lowercase.
    visitno = models.IntegerField(db_column='VisitNo')  # Field name made lowercase.
    medtype = models.SmallIntegerField(db_column='MedType')  # Field name made lowercase.
    source = models.IntegerField(db_column='Source')  # Field name made lowercase.
    trancode = models.CharField(db_column='TranCode', max_length=1)  # Field name made lowercase.
    vsdrno = models.SmallIntegerField(db_column='VsDrNo')  # Field name made lowercase.
    orderuser = models.SmallIntegerField(db_column='OrderUser')  # Field name made lowercase.
    ordertime = models.DateTimeField(db_column='OrderTime')  # Field name made lowercase.
    preexectime = models.DateTimeField(db_column='PreExecTime')  # Field name made lowercase.
    preexecloc = models.SmallIntegerField(db_column='PreExecLoc')  # Field name made lowercase.
    preexecbed = models.SmallIntegerField(db_column='PreExecBed')  # Field name made lowercase.
    medsummary = models.TextField(db_column='MedSummary')  # Field name made lowercase.
    medoptions = models.CharField(db_column='MedOptions', max_length=30)  # Field name made lowercase.
    expandtime = models.DateTimeField(db_column='ExpandTime')  # Field name made lowercase.
    exectype = models.CharField(db_column='ExecType', max_length=2)  # Field name made lowercase.
    execno = models.IntegerField(db_column='ExecNo')  # Field name made lowercase.
    execuser = models.SmallIntegerField(db_column='ExecUser')  # Field name made lowercase.
    exectime = models.DateTimeField(db_column='ExecTime')  # Field name made lowercase.
    execloc = models.SmallIntegerField(db_column='ExecLoc')  # Field name made lowercase.
    createuser = models.SmallIntegerField(db_column='CreateUser')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    newmedtype = models.SmallIntegerField(db_column='NewMedType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MedOrder'


class Visitrecord(models.Model):
    app_label = 'AIC8'
    visitno = models.AutoField(db_column='VisitNo', primary_key=True)  # Field name made lowercase.
    chartno = models.IntegerField(db_column='ChartNo')  # Field name made lowercase.
    visitdate = models.DateTimeField(db_column='VisitDate')  # Field name made lowercase.
    visitzone = models.CharField(db_column='VisitZone', max_length=1)  # Field name made lowercase.
    visittype = models.CharField(db_column='VisitType', max_length=2)  # Field name made lowercase.
    visitseqno = models.CharField(db_column='VisitSeqNo', max_length=4)  # Field name made lowercase.
    pttype = models.CharField(db_column='PtType', max_length=1)  # Field name made lowercase.
    discounttype = models.SmallIntegerField(db_column='DiscountType')  # Field name made lowercase.
    casetype = models.CharField(db_column='CaseType', max_length=2)  # Field name made lowercase.
    paytype = models.CharField(db_column='PayType', max_length=1)  # Field name made lowercase.
    parttype = models.CharField(db_column='PartType', max_length=3)  # Field name made lowercase.
    isupload = models.BooleanField(db_column='IsUpload')  # Field name made lowercase.
    nhiseqno = models.SmallIntegerField(db_column='NhiSeqNo')  # Field name made lowercase.
    checkuser = models.SmallIntegerField(db_column='CheckUser')  # Field name made lowercase.
    checktime = models.DateTimeField(db_column='CheckTime')  # Field name made lowercase.
    updateuser = models.SmallIntegerField(db_column='UpdateUser')  # Field name made lowercase.
    updatetime = models.DateTimeField(db_column='UpdateTime')  # Field name made lowercase.
    paystatus = models.CharField(db_column='PayStatus', max_length=1)  # Field name made lowercase.
    isrealfirstvisit = models.BooleanField(db_column='IsRealFirstVisit')  # Field name made lowercase.
    pactype = models.SmallIntegerField(db_column='PacType')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'VisitRecord'
        unique_together = (('visitno', 'chartno'),)

