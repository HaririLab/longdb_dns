# ## run these from within a django shell:
# ## python3 manage.py shell < DataToIncorporate/import_battery.py

import csv, datetime
from decimal import Decimal
from getdata.models import Subject, BatteryVariable, BatteryValue
from itertools import islice

# read battery data from additional file
with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/DNS_DDT.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	print(row1[0])
	for row in reader:
	# for row in islice(reader,977,None): # for starting in the middle
		print(row[0])
		s,c=Subject.objects.get_or_create(dns_id=row[0])
		for i in range(1,len(row1)):
			name_str=row1[i]
			name_list=name_str.split("_")
			# r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type='RAW')
			if name_list[-1] == 'RAW' or name_list[-1] == 'REC':
				r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type=name_list[-1])
			else:
				r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type='.')
			# add value to db if not empty
			if row[i].strip(' "') and row[i] != '.':
				v=BatteryValue.objects.create(subject=s,variable=r,value=Decimal(row[i].strip(' "')))
			else:
				v=BatteryValue.objects.create(subject=s,variable=r,value=None)
		s.save();

# # read battery data from main file
# with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/BATTERY_RAW.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	print(row1[0])
# 	for row in reader:
# 	# for row in islice(reader,977,None): # for starting in the middle
# 		print(row[0])
# 		s,c=Subject.objects.get_or_create(dns_id=row[0])
# 		if row[1] == '1':
# 			s.gender='M';
# 		elif row[1] =='2':
# 			s.gender='F';
# 		else:
# 			continue
# 		s.race_battery=row[2];
# 		s.latino_battery=row[3];
# 		s.age=row[4];
# 		for i in range(1,len(row1)):
# 			name_str=row1[i]
# 			name_list=name_str.split("_")
# 			# r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type='RAW')
# 			if name_list[-1] == 'RAW' or name_list[-1] == 'REC':
# 				r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type=name_list[-1])
# 			else:
# 				r,c=BatteryVariable.objects.get_or_create(var_name=name_str,var_type='.')
# 			# add value to db if not empty
# 			if row[i].strip(' "'):
# 				v=BatteryValue.objects.create(subject=s,variable=r,value=Decimal(row[i].strip(' "')))
# 			else:
# 				v=BatteryValue.objects.create(subject=s,variable=r,value=None)
# 		s.save();

# # changing variable name so that it doesn't conflict with RAW/REC naming convention
# newvar, created=BatteryVariable.objects.get_or_create(var_name='EDI_Bul_unscaled',var_type='.')
# newvar.save()
# oldvar=BatteryVariable.objects.get(var_name='EDI_Bul_raw') #EDI_Thn_raw EDI_Bdd_raw
# for val in BatteryValue.objects.filter(variable=oldvar):
# 	val.variable=newvar
# 	val.save()
# oldvar.delete()

# # change variable name for subjects (pre 1123) with weird numbering
# # NOTE: shouldn't need anymore bc I changed this in the BATTERY_RAW.csv
# newvar=BatteryVariable.objects.get(var_name='Sex_1_RAW')
# oldvar=BatteryVariable.objects.get(var_name='Sex_1.0_RAW')
# for val in BatteryValue.objects.filter(variable=oldvar):
# 	val.variable=newvar
# 	val.save()
# oldvar.delete()

#####################################OLD######################################

# # first time I imported I didn't fill in NULL values, so do taht here
# subjects=Subject.objects.all()
# batvars=BatteryVariable.objects.all()
# for s in subjects:
# 	for v in batvars:
# 		# check if exists
# 		found=BatteryValue.objects.filter(subject=s,variable=v)
# 		if found.count() == 0:
# 			BatteryValue.objects.create(subject=s,variable=v,value=None)

# # faces or cards data
# ## ##Variable names (column headings) MUST be of the format Task_Contrast_ROI!!!!!!!!
# import datetime, csv
# from decimal import Decimal
# from getdata.models import Subject, ImagingVariable, ImagingValue
# task="Cards"
# with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/cards.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		print(row[0])
# 		s,c=Subject.objects.get_or_create(dns_id=row[0])
# 		# print(row[0])
# 		for i in range(1,len(row1)):
# 			r,c=ImagingVariable.objects.get_or_create(var_name=row1[i],vargroup=task)
# 			if(row[i]):
# 				g=ImagingValue.objects.create(subject=s,variable=r,value=row[i])
# 			else:
# 				g=ImagingValue.objects.create(subject=s,variable=r,value=None)

# # Day 1 data
# ## ##Variable names (column headings) MUST be of the format Task_Contrast_ROI!!!!!!!!
# import datetime, csv
# from decimal import Decimal
# from getdata.models import Subject, Day1Variable, Day1Value
# with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/day1.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		print(row[0])
# 		s,c=Subject.objects.get_or_create(dns_id=row[0])
# 		for i in range(1,len(row1)):
# 			r,c=Day1Variable.objects.get_or_create(var_name=row1[i])
# 			if(row[i]):
# 				g=Day1Value.objects.create(subject=s,variable=r,value=row[i])
# 			else:
# 				g=Day1Value.objects.create(subject=s,variable=r,value=None)

# # SNP details
# # this will probably taken an hour or so
# import csv, math
# from getdata.models import SNP, Subject, Genotype
# with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/plink.frq.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	for row in reader:
# 		snp,c = SNP.objects.get_or_create(rs_id=row[1])#,a1=a1,a2=a2,chr_id=chr_num)
# 		if row[2] == '1':
# 			snp.a1='A'
# 		elif row[2] == '2':
# 			snp.a1='C'
# 		elif row[2] == '3':
# 			snp.a1='G'
# 		elif row[2] == '4':
# 			snp.a1='T'
# 		else:
# 			snp.a1=row[2]
# 		if row[3] == '1':
# 			snp.a2='A'
# 		elif row[3] == '2':
# 			snp.a2='C'
# 		elif row[3] == '3':
# 			snp.a2='G'
# 		elif row[3] == '4':
# 			snp.a2='T'
# 		else:
# 			snp.a2=row[3]
# 		if row[4] == 'NA':
# 			snp.MAF = -1;
# 		else:
# 			snp.MAF=row[4]
# 		snp.nchrobs=math.floor(int(row[5])/2374*100)
# 		snp.chr_id=row[0]
# 		snp.save()
# 		# print(snp.rs_id)

# fill in NULL img values
### MUST run this if the csv file used for importing imaging data only includes subjects with good data
# from getdata.models import Subject, ImagingVariable, ImagingValue
# subjects=Subject.objects.all()
# imgvars=ImagingVariable.objects.all()
# for s in subjects:
# 	for v in imgvars:
# 		# check if exists
# 		found=ImagingValue.objects.filter(subject=s,variable=v)
# 		if found.count() == 0:
# 			ImagingValue.objects.create(subject=s,variable=v,value=None)

# # fill in NULL bat values
# ### MUST run this if the csv file used for importing imaging data only includes subjects with good data
# from getdata.models import Subject, BatteryVariable, BatteryValue
# subjects=Subject.objects.all()
# imgvars=BatteryVariable.objects.all()
# for s in subjects:
# 	for v in imgvars:
# 		# check if exists
# 		found=BatteryValue.objects.filter(subject=s,variable=v)
# 		if found.count() == 0:
# 			BatteryValue.objects.create(subject=s,variable=v,value=None)
