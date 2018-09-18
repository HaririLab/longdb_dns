from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from getdata.models import Subject, SNP, Genotype
from getdata.forms import SelectionForm_SNP

@login_required(login_url="/longdb_dns/login/")
def checkSNP(request):
	if request.method == 'POST':
		form_snp = SelectionForm_SNP(request.POST)
		if form_snp.is_valid():
			
			snps=[]
			if form_snp.cleaned_data['rsIDs']: 
				for rsID in form_snp.cleaned_data['rsIDs']:
					snps.append(SNP.objects.get(rs_id=rsID))  

			return render(request, 'checkSNP_output.html',{'snps':snps})

	else:
		form_snp = SelectionForm_SNP()

	return render(request, 'checkSNP_input.html',{'form_snp':form_snp})
