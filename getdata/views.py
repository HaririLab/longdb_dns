from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import *
from functools import reduce
from django.db.models import Q, Prefetch
from getdata.more_functions import get_img_subvars, get_day1_subvars, get_bat_subvars

from .models import Subject, SNP, Genotype, BatteryVariable, BatteryValue, ImagingVariable, ImagingValue, Day1Variable, Day1Value
from .forms import SelectionForm, SelectionForm_Battery, SelectionForm_Imaging, SelectionForm_SNP, SelectionForm_Day1

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
# @login_required(login_url="/login/")
# def home(request):
# 	# return render(request, "home.html", {'subjects': Subject.objects.all()})
# 	return render(request, "home.html")

@login_required(login_url="/login/")
def select(request):
	if request.method == 'POST':
		form = SelectionForm(request.POST)
		form_day1 = SelectionForm_Day1(request.POST)
		form_bat = SelectionForm_Battery(request.POST)
		form_img = SelectionForm_Imaging(request.POST)
		form_snp = SelectionForm_SNP(request.POST)
		if form.is_valid() and form_bat.is_valid() and form_img.is_valid() and form_snp.is_valid() and form_day1.is_valid():
			fields=[]
			if form.cleaned_data['useGender']:
				fields.append('gender')
			if form.cleaned_data['useRace']:
				fields.append('race_battery')
			if form.cleaned_data['useAge']:
				fields.append('age')	
			
			subjects = Subject.objects.all().order_by('dns_id') #[0:10]	########## i guess i get rid of this and just prefetch from each table with the same base query?!?!? wait actually i need subjects to prepopulate blank array; maybe i can make it a queryset or something that i use for each of the following

			vars_day1=[]
			fields_day1=[]
			for requested_var in form_day1.cleaned_data['day1_selections']:
				for subvar in get_day1_subvars(requested_var):
					vars_day1.append(Day1Variable.objects.get(var_name=subvar))  
					fields_day1.append(subvar)
			if(len(vars_day1)>0):
				subjects_day1=subjects.prefetch_related(  
				    Prefetch(
				            'day1val',
				            queryset=Day1Value.objects.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_day1])),
				            to_attr='day1vals'
				    )
				)		
				subjects_day1 = list(subjects_day1)
				indices=[fields_day1.index(subjects_day1[0].day1vals[i].variable_id) for i in range(0,len(fields_day1))]
				indices_rev=[indices.index(i) for i in range(0, len(indices))]
				vals_day1=[[s.day1vals[i] for i in indices_rev] for s in subjects_day1]
			else:
				vals_day1=[[] for s in subjects] # need this for zip to work later	


			vars_bat=[]
			fields_bat=[]
			for requested_var in form_bat.cleaned_data['battery_selections']:
				for subvar in get_bat_subvars(requested_var):
					vars_bat.append(BatteryVariable.objects.get(var_name=subvar))  
					fields_bat.append(subvar)
			# much faster!
			if(len(vars_bat)>0):
				subjects_bat=subjects.prefetch_related(  # filter(gender='F').
				    Prefetch(
				            'batval',
				            queryset=BatteryValue.objects.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_bat])),
				            to_attr='batvals'
				    )
				)		
				subjects_bat = list(subjects_bat)
				indices=[fields_bat.index(subjects_bat[0].batvals[i].variable_id) for i in range(0,len(fields_bat))]
				indices_rev=[indices.index(i) for i in range(0, len(indices))]
				vals_bat=[[s.batvals[i] for i in indices_rev] for s in subjects_bat]
			else:
				vals_bat=[[] for s in subjects] # need this for zip to work later

			vars_img=[]
			fields_img=[]
			for requested_var in form_img.cleaned_data['imaging_selections']:
				for subvar in get_img_subvars(requested_var):
					vars_img.append(ImagingVariable.objects.get(var_name=subvar))  
					fields_img.append(subvar)
			if(len(vars_img)>0):
				subjects_img=subjects.prefetch_related(  # filter(gender='F').
				    Prefetch(
				            'imgval',
				            queryset=ImagingValue.objects.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_img])),
				            to_attr='imgvals'
				    )
				)		
				subjects_img = list(subjects_img)
				indices=[fields_img.index(subjects_img[0].imgvals[i].variable_id) for i in range(0,len(fields_img))]
				indices_rev=[indices.index(i) for i in range(0, len(indices))]
				vals_img=[[s.imgvals[i] for i in indices_rev] for s in subjects_img] ###### this line changes the order of s.imgvals if more than one con_ROI is selected!!!!!				
			else:
				vals_img=[[] for s in subjects] # need this for zip to work later
			
			snps=[]
			fields_snp=[]
			if form_snp.cleaned_data['rsIDs']: 
				for rsID in form_snp.cleaned_data['rsIDs']:
					snp=SNP.objects.get(rs_id=rsID)
					snps.append(snp)  
					fields_snp.append(rsID+'_'+snp.a1+'('+snp.a2+')')
			## with prefetch
			genos=[]
			if(len(snps)>0):
				subjects_gen=subjects.prefetch_related(  # filter(gender='F').
				    Prefetch(
				            'genotype',
				            queryset=Genotype.objects.filter(reduce(lambda x, y: x | y, [Q(SNP=snp) for snp in snps])),
				            to_attr='genotypes'
				    )
				)
				##### ideally only need this before all SNP data is populated... not sure how it'll handle case where a subj has one of the requested SNPs but not all!
				for s in subjects_gen:
					if s.genotypes:
						genos.append(s.genotypes)  #### not sure why i have to use genotype rather than genotype_set here bc the opposite was what worked in the shelL!
					else:
						genos.append('None')
			else:
				genos=[[] for s in subjects] # need this for zip to work later		

			subj_data_tuples=list(zip(subjects,vals_day1,vals_bat,vals_img,genos)	)

			if request.POST['action'] == 'Preview':
				#### need to do a bit more research to enable adding the "write csv" button to preview page
				# request.session['context_data'] = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
				# print(request.session['context_data'])
				# print('****0******')
				return render(request, 'selected_data.html',{'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples})
			else:
				# try:	
				# 	print('********1*********')
				# 	print(fields_day1,subj_data_tuples)
				# 	print(request.session['context_data'])
				# 	subj_data_tuples,fields,fields_img,fields_day1,fields_bat,fields_snp # check if this is already defined, won't work bc these are defined but empty (excpet subjects)
				# 	context_data = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
				# except:
				# 	print('********2*********')
				# 	context_data = request.session['context_data']  # if not, 
				response = HttpResponse(content_type='text/csv')
				response['Content-Disposition'] = 'attachment; filename="ExtractedData.csv"'
				t = loader.get_template('write_csv_template.py')
				# response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
				response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
				return response

		else:
			messages.error(request,"Error", extra_tags='alert')

	else:
		form = SelectionForm()
		form_day1 = SelectionForm_Day1()
		form_bat = SelectionForm_Battery()
		form_img = SelectionForm_Imaging()
		form_snp = SelectionForm_SNP()

	return render(request, 'select.html',{'form':form,'form_day1':form_day1,'form_bat':form_bat,'form_img':form_img,'form_snp':form_snp})
