# ## run these from within a django shell:
# ## python3 manage.py shell < DataToIncorporate/import_Composite.py

import csv, datetime
from decimal import Decimal
from getdata.models import Subject, CompositeVariable, CompositeValue
from itertools import islice

with open('/home/rapiduser/longdb_dns/DataToIncorporate/DNS_compositeScores.csv',newline='') as f:
	reader=csv.reader(f)
	row1=next(reader)
	print(row1[0])
	for row in reader:
		print(row[0])
		s,c=Subject.objects.get_or_create(dns_id=row[0])
		for i in range(1,len(row1)):
			name_str=row1[i]
			r,c=CompositeVariable.objects.get_or_create(var_name=name_str)
			# add value to db if not empty
			if row[i].strip(' "') and row[i] != '.':
				v=CompositeValue.objects.create(subject=s,variable=r,value=Decimal(row[i].strip(' "')))
			else:
				v=CompositeValue.objects.create(subject=s,variable=r,value=None)
		s.save();
