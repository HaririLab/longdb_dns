# ## run these from within a django shell:
# ## python3 manage.py shell < DataToIncorporate/import_Imaging.py

# ## Imaging
import datetime, csv
import glob
from decimal import Decimal
from getdata.models import Subject, ImagingValue, ImagingVariable
# files=glob.glob('/home6/haririla/public_html/longdb_dns/DataToIncorporate/Imaging/Free*.csv')
#file='/home6/haririla/public_html/longdb_dns/DataToIncorporate/DNS_DTI_ENIGMA_ROI_extracted.csv'
file='/home6/haririla/public_html/longdb_dns/DataToIncorporate/DNS_MRI_covariates_num.csv'

#task="DTI.FA.ENIGMA.ROI" #"Covariates"
task="Covariates"
string="no" # "yes" e.g. for paths and non-numeric covariates

with open(file,newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	ct=0;
	for row in reader:
		ct=ct+1
		# if ct>10:
		# 	break
		print(row[0])
		s,c=Subject.objects.get_or_create(dns_id=row[0])
		for i in range(1,len(row1)):
			var=row1[i]
			# try:
			if(task=="Covariates"):
				r,c=ImagingVariable.objects.get_or_create(var_name="Covs_"+var,vargroup=task)
			elif(task=="DTI.FA.ENIGMA.ROI"):
				r,c=ImagingVariable.objects.get_or_create(var_name="FA.ENIGMA_"+var,vargroup=task)
			else:
				r,c=ImagingVariable.objects.get_or_create(var_name=task+"_"+var,vargroup=task)
			if(row[i]):
				if(row[i]=="NA" or row[i]=="." ):
					g=ImagingValue.objects.create(subject=s,variable=r,value=None)			
				else:
					if(string=="yes"):
						g=ImagingValue.objects.create(subject=s,variable=r,value=99999,path=row[i])			
					else:
						g=ImagingValue.objects.create(subject=s,variable=r,value=row[i])			
			else:
				g=ImagingValue.objects.create(subject=s,variable=r,value=None)		
			# except:
			# 	print("Error with "+s.dns_id+" "+var)
			# 	break

# fill in NULL img values
### MUST run this if the csv file used for importing imaging data only includes subjects with good data
from getdata.models import Subject, ImagingValue, ImagingVariable
subjects=Subject.objects.all()
imgvars=ImagingVariable.objects.all()
for s in subjects:
	for v in imgvars:
		# check if exists
		found=ImagingValue.objects.filter(subject=s,variable=v)
		if found.count() == 0:
			ImagingValue.objects.create(subject=s,variable=v,value=None)
