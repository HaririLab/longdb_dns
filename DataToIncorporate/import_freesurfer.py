# ## run these from within a django shell:
# ## python3 manage.py shell < DataToIncorporate/import_freesurfer.py

# ## FreeSurfer
import datetime, csv
import glob
from decimal import Decimal
from getdata.models import Subject, FreeSurferValue, FreeSurferVariable
files=glob.glob('/home/rapiduser/longdb_dns/DataToIncorporate/FreeSurfer/Free*.csv')
for file in files:
	skipfile=0
	print(file)
	task=file.split('/')[-1].replace('.csv','').replace('FreeSurfer_','')
	task_short=task.replace('aparc.DKTatlas40_','DKT').replace('aparc.a2009s_','Dest').replace('aparc_','DK').replace('aseg_Volume_mm3','asegVol')
	task_short=task_short.replace('Gray','').replace('SurfArea','SA').replace('ThickAvg','CT')
	with open(file,newline='') as f:
		reader=csv.reader(f)
		row1=next(reader)
		# ct=0;
		for row in reader:
			# ct=ct+1
			# if ct>999:
			# 	continue				
			if skipfile==1:
				break
			print(row[0])
			s,c=Subject.objects.get_or_create(dns_id=row[0])
			for i in range(1,len(row1)):
				if 'aseg' in file:
					if 'Right-' in row1[i]:
						roi=row1[i].replace('Right-','')+'.R'
					elif 'Left-' in row1[i]:
						roi=row1[i].replace('Left-','')+'.L'
				elif 'wmparc' in file:
					if 'wm-lh' in row1[i]:
						roi=row1[i].replace('wm-lh','wm')+'.L'
					elif 'wm-rh' in row1[i]:
						roi=row1[i].replace('wm-rh','wm')+'.R'	
				else:
					roi=row1[i].replace('_left','.L').replace('_right','.R')
				try:
					r,c=FreeSurferVariable.objects.get_or_create(var_name=task_short+"."+roi,vargroup=task)
					if(row[i]):
						if(row[i]=="NA"):
							g=FreeSurferValue.objects.create(subject=s,variable=r,value=None)			
						else:
							g=FreeSurferValue.objects.create(subject=s,variable=r,value=row[i])			
					else:
						g=FreeSurferValue.objects.create(subject=s,variable=r,value=None)	
				except:
					print("Error with "+s.dns_id+" "+roi)

# fill in NULL img values
### MUST run this if the csv file used for importing imaging data only includes subjects with good data
from getdata.models import Subject, FreeSurferValue, FreeSurferVariable
subjects=Subject.objects.all()
imgvars=FreeSurferVariable.objects.all()
for s in subjects:
	for v in imgvars:
		# check if exists
		found=FreeSurferValue.objects.filter(subject=s,variable=v)
		if found.count() == 0:
			FreeSurferValue.objects.create(subject=s,variable=v,value=None)
