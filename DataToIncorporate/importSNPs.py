
# read CSV where first column is DNSID, first row is header row straight from plink: id in column 2, and genos start in 7
# assuming SNP details have already been imported from plink.frq
import csv, time
from getdata.models import SNP, Subject, Genotype

def main():
	snps=SNP.objects.filter(chr_id=1)
	genos=[]
	t1=time.time()
	with open('/home6/haririla/public_html/longtest/chr1_5subs.csv',newline='') as f:
		reader=csv.reader(f)
		row1=next(reader)
		for row in reader:
			s=Subject.objects.get(dns_id=row[1])
			for i in range(6,len(row1)):  #### starting with 6 bc of extra plink columns!!
				[rsid,allele]=row1[i].split("_")
				snp = snps.get(rs_id=rsid)
				geno = Genotype(subject=s,SNP=snp,genotype=row[i])  #### subtracting 6 bc of extra plink columns!!
				genos.append(geno)
	print("finished reading csv, elapsed time: "+str(time.time()-t1))
	# the above took about 30 minutes, while the below took 10ish seconds
	Genotype.objects.bulk_create(genos)
	print("finished inserting genos, elapsed time: "+str(time.time()-t1))





# ## dont really need this anymore since i loaded all the SNP info from the plink.frq file
# import csv
# from getdata.models import SNP, Subject, Genotype
# chr_num=1
# with open('../chr1_5subs.csv',newline='') as f:
# 	reader=csv.reader(f)
# 	row1=next(reader)
# 	snps=[]
# 	for i in range(6,len(row1)):
# 		[rsid,allele]=row1[i].split("_")
# 		a1=allele[0]
# 		a2=allele[3]
# 		snp = SNP(rs_id=rsid,a1=a1,a2=a2,chr_id=chr_num)
# 		snps.append(snp)
# # the above takes under a second, while the below takes 4 or 5 seconds (for chr1)
# SNP.objects.bulk_create(snps)
