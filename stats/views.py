from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import *
from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import ColumnChart
from functools import reduce
from django.db.models import Q, Prefetch
from getdata.more_functions import get_img_subvars, get_day1_subvars

from getdata.models import Subject, SNP, Genotype, BatteryVariable, BatteryValue, ImagingVariable, ImagingValue, Day1Variable, Day1Value
from getdata.forms import SelectionForm, SelectionForm_Battery, SelectionForm_Imaging, SelectionForm_SNP, SelectionForm_Day1


@login_required(login_url="/login/")
def stats(request):
	if request.method == 'POST':
		form_bat = SelectionForm_Battery(request.POST)
		form_snp = SelectionForm_SNP(request.POST)
		if form_bat.is_valid() and form_snp.is_valid():
			
			subjects = Subject.objects.all()	

			#### must only be one var / field - need to check for / change this!!!	
			field_bat=form_bat.cleaned_data['battery_selections'][0]
			var_bat=BatteryVariable.objects.get(var_name=field_bat)
			# val_objs_bat=[s.batval.get(variable=var_bat) for s in subjects] ######
			# vals_bat=[v.value for v in val_objs_bat]

			#### must only be one var / field - need to check for / change this!!!
			field_snp=form_snp.cleaned_data['rsIDs'][0]
			snp=SNP.objects.get(rs_id=field_snp)			
			alleles=[snp.a1+snp.a1,snp.a1+snp.a2,snp.a2+snp.a2]

			pairs=[]
			for s in subjects:
				if s.genotype.filter(SNP=snp).count() == 1:
					g=s.genotype.get(SNP=snp)
					if g.genotype == '0' or g.genotype == '1' or g.genotype == '2': # not NA or missing
						if s.batval.filter(variable=var_bat).count() == 1:
							v=s.batval.get(variable=var_bat)
							if v.value != None:
								pairs.append([v.value,g.genotype])
			# geno_objs=[s.genotype.get(SNP=snp) for s in subjects] #### not sure why i have to use genotype rather than genotype_set here bc the opposite was what worked in the shelL!
			# genos=[g.genotype for g in geno_objs]

			# pairs=list(zip(vals_bat,genos))  #### might work without the list bit but this was easier to work with in the shell
			g_vals=[]
			# gs=set(genos) #set([pairs[i][1] for i in range(0,len(pairs))]) # if use this need to double check order
			gs=['0','1','2'] # do it in reverse bc using append 
			graph_array=[['Genotype',field_bat]] # for graphos
			# calculate average of batval for each geno
			counts=[]
			for g in gs: 
				cur_vals=[p[0] for p in pairs if p[1]==g]
				if len(cur_vals) == 0:
					cur_avg=0
				else:
					cur_avg=sum(cur_vals)/Decimal(len(cur_vals))
				g_vals.append(cur_avg)
				graph_array.append([alleles[int(g)],cur_avg]) # for graphos # prob not best way to get alleles
				counts.append(len(cur_vals))
			
			# plotting with graphos
			chart = ColumnChart(SimpleDataSource(data=graph_array),options={'title': field_bat + ' by ' + field_snp + ' genotype'})	

			# return render(request, 'selected_stats.html',{'field_bat':field_bat,'field_snp':field_snp,'val_by_g':val_by_g,'script':script,'div':div})
			return render(request, 'selected_stats.html',{'field_bat':field_bat,'field_snp':field_snp,'counts':counts,'alleles':alleles,'chart':chart})

	else:
		form_bat = SelectionForm_Battery()
		form_snp = SelectionForm_SNP()

	return render(request, 'selection_stats.html',{'form_bat':form_bat,'form_snp':form_snp})

