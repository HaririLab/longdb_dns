## run these from within a django shell:
## python3 manage.py shell

# SNP details
import csv, math
from getdata.models import SNP, Subject, Genotype
with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/plink.frq.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	for row in reader:
		snp,c = SNP.objects.get_or_create(rs_id=row[1])#,a1=a1,a2=a2,chr_id=chr_num)
		if row[2] == '1':
			snp.a1='A'
		elif row[2] == '2':
			snp.a1='C'
		elif row[2] == '3':
			snp.a1='G'
		elif row[2] == '4':
			snp.a1='T'
		else:
			snp.a1=row[2]
		if row[3] == '1':
			snp.a2='A'
		elif row[3] == '2':
			snp.a2='C'
		elif row[3] == '3':
			snp.a2='G'
		elif row[3] == '4':
			snp.a2='T'
		else:
			snp.a2=row[3]
		if row[4] == 'NA':
			snp.MAF = -1;
		else:
			snp.MAF=row[4]
		snp.nchrobs=math.floor(int(row[5])/2374*100)
		snp.chr_id=row[0]
		snp.save()
		# print(snp.rs_id)
		


# real battery data
import csv, datetime
from decimal import Decimal
from getdata.models import Subject, BatteryVariable, BatteryValue
from itertools import islice
with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/BATTERY_SCORED_formatted.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	for row in reader:
	#for row in islice(reader,344,None): # for starting in the middle
		print(row[0])
		s,c=Subject.objects.get_or_create(dns_id=row[0])
		if row[1] == '1':
			s.gender='M';
		elif row[1] =='2':
			s.gender='F';
		else:
			continue
		s.race_battery=row[2];
		s.latino_battery=row[3];
		s.age=row[4];		
		for i in range(5,len(row1)):
			r,c=BatteryVariable.objects.get_or_create(var_name=row1[i])
			# add value to db if not empty
			if row[i].strip(' "'):
				v=BatteryValue.objects.create(subject=s,variable=r,value=Decimal(row[i].strip(' "')))	
			else:
				v=BatteryValue.objects.create(subject=s,variable=r,value=None)	
		s.save();

# # first time I imported I didn't fill in NULL values, so do taht here
# subjects=Subject.objects.all()
# batvars=BatteryVariable.objects.all()
# for s in subjects:
# 	for v in batvars:
# 		# check if exists
# 		found=BatteryValue.objects.filter(subject=s,variable=v)
# 		if found.count() == 0:
# 			BatteryValue.objects.create(subject=s,variable=v,value=None)



# faces data
import datetime, csv
with open('/Users/Annchen/DjangoProjects/longdb_dns/DataToIncorporate/Hammer.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	for row in reader:
		s,c=Subject.objects.get_or_create(dns_id=row[0])
		# print(row[0])
		for i in range(1,len(row1)):
			r,c=ImagingVariable.objects.get_or_create(var_name=row1[i])
			if(row[i]):
				g=ImagingValue.objects.create(subject=s,variable=r,value=row[i])			
			else:
				g=ImagingValue.objects.create(subject=s,variable=r,value=None)			

# fill in NULL img values
subjects=Subject.objects.all()
imgvars=ImagingVariable.objects.all()
for s in subjects:
	for v in imgvars:
		# check if exists
		found=ImagingValue.objects.filter(subject=s,variable=v)
		if found.count() == 0:
			ImagingValue.objects.create(subject=s,variable=v,value=None)


from functools import reduce
from django.db.models import Q, Prefetch
from getdata.models import ImagingValue,ImagingVariable
vars_img=[]
fields_img=[]
requested_vars=('Cards_NegGrCtrl_LVS_clust','Cards_NegGrCtrl_LVS_vox','Cards_PosGrCtrl_LVS_clust','Cards_PosGrCtrl_LVS_vox')
for requested_var in requested_vars:
	vars_img.append(ImagingVariable.objects.get(var_name=requested_var))  
	fields_img.append(requested_var)
if(len(vars_img)>0):
	subjects_img=subjects.prefetch_related(  # filter(gender='F').
	    Prefetch(
	            'imgval',
	            queryset=ImagingValue.objects.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_img])),
	            to_attr='imgvals'
	    )
	)	
	indices=[fields_img.index(subjects_img[0].imgvals[i].variable_id) for i in range(0,len(vars_img))]
	vals_img=[list(s.imgvals[i] for i in indices) for s in subjects_img] 


