from django.db import models
from decimal import Decimal

class Subject(models.Model):
	dns_id = models.CharField(max_length = 10,unique=True,primary_key=True)
	gender = models.CharField(max_length = 2,default='.')
	race_battery = models.CharField(max_length = 2,default='.')
	latino_battery = models.CharField(max_length = 2,default='.')
	age = models.IntegerField(default=-1)

	def getattribute(self,attr):
		return getattr(self,attr)

	def __str__(self):
		return self.dns_id 	

class ImagingVariable(models.Model):
	var_name = models.CharField(max_length=50,unique=True,primary_key=True)
	subjects = models.ManyToManyField(Subject,through='ImagingValue')

	def __str__(self):
		return self.var_name

class ImagingValue(models.Model):
	subject = models.ForeignKey(Subject,related_name='imgval',on_delete=models.DO_NOTHING)
	variable = models.ForeignKey(ImagingVariable,on_delete=models.DO_NOTHING)
	value = models.DecimalField(decimal_places=5,max_digits=12,null=True)

	def __str__(self):
		return self.subject.dns_id + '_' + self.variable.var_name

class BatteryVariable(models.Model):
	var_name = models.CharField(max_length=32,unique=True,primary_key=True)
	subjects = models.ManyToManyField(Subject,through='BatteryValue')

	def __str__(self):
		return self.var_name

class BatteryValue(models.Model):
	subject = models.ForeignKey(Subject,related_name='batval',on_delete=models.DO_NOTHING)
	variable = models.ForeignKey(BatteryVariable,on_delete=models.DO_NOTHING)
	value = models.DecimalField(decimal_places=5,max_digits=12,null=True)

	def __str__(self):
		return self.subject.dns_id + '_' + self.variable.var_name

class Day1Variable(models.Model):
	var_name = models.CharField(max_length=32,unique=True,primary_key=True)
	subjects = models.ManyToManyField(Subject,through='Day1Value')

	def __str__(self):
		return self.var_name		

class Day1Value(models.Model):
	subject = models.ForeignKey(Subject,related_name='day1val',on_delete=models.DO_NOTHING)
	variable = models.ForeignKey(Day1Variable,on_delete=models.DO_NOTHING)
	value = models.CharField(max_length=150,null=True)

	def __str__(self):
		return self.subject.dns_id + '_' + self.variable.var_name

class SNP(models.Model):
	rs_id = models.CharField(max_length=32,unique=True,primary_key=True)
	subjects = models.ManyToManyField(Subject,through='Genotype')
	a1 = models.CharField(max_length=2,default='.')
	a2 = models.CharField(max_length=2,default='.')
	MAF = models.DecimalField(decimal_places=2,max_digits=4,default=Decimal('-1.0'))
	chr_id = models.IntegerField(default=-1)
	nchrobs = models.IntegerField(default=-1) # number of chromosone observations
	def __str__(self):
		return self.rs_id + '_' + self.a1 + '(' + self.a2 + ')'

class Genotype(models.Model):
	subject = models.ForeignKey(Subject,related_name='genotype',on_delete=models.DO_NOTHING)
	SNP = models.ForeignKey(SNP,on_delete=models.DO_NOTHING)
	genotype = models.CharField(max_length=2)

	def __str__(self):
		return self.subject.dns_id + '_' + self.SNP.rs_id
