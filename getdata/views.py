from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader, Context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import *
from functools import reduce
from django.db.models import Q, Prefetch
from getdata.more_functions import run_query #get_img_subvars, get_day1_subvars, get_bat_subvars

from .models import Subject, SNP, Genotype, BatteryVariable, BatteryValue, ImagingVariable, ImagingValue, Day1Variable, Day1Value
from .forms import SelectionForm, SelectionForm_SNP, SelectionForm_bat_type

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")

@login_required(login_url="/longdb_dns/login/")
def select(request):
    if request.method == 'POST':
        if request.POST['action'] == 'Write CSV now':
            return HttpResponse("You'd switch to Write CSV mode now.")
        form = SelectionForm(request.POST)
        # form_day1 = SelectionForm_Day1(request.POST)
        # form_bat = SelectionForm_Battery(request.POST)
        # form_img = SelectionForm_Imaging(request.POST)
        form_snp = SelectionForm_SNP(request.POST)
        form_bat_type = SelectionForm_bat_type(request.POST)
        if form.is_valid() and form_snp.is_valid() and form_bat_type.is_valid():
            fields=[]
            if form.cleaned_data['useGender']:
                fields.append('gender')
            if form.cleaned_data['useRace']:
                fields.append('race_battery')
            if form.cleaned_data['useAge']:
                fields.append('age')

            bat_type=[]
            if form_bat_type.cleaned_data['useSCORE']:
                bat_type.append('.')
            if form_bat_type.cleaned_data['useREC']:
                bat_type.append('REC')
            if form_bat_type.cleaned_data['useRAW']:
                bat_type.append('RAW')

            subjects = Subject.objects.all().order_by('dns_id') #[0:10]    ########## i guess i get rid of this and just prefetch from each table with the same base query?!?!? wait actually i need subjects to prepopulate blank array; maybe i can make it a queryset or something that i use for each of the following

            # fields_day1,vals_day1=run_query(request.POST.getlist('day1_selections'),"day1",subjects)
            # fields_bat,vals_bat=run_query(request.POST.getlist('bat_selections'),"bat",subjects)
            # fields_img,vals_img=run_query(request.POST.getlist('img_selections'),"img",subjects)
            ### edit for bat var_type
            fields_day1,vals_day1=run_query(request.POST.getlist('day1_selections'),"day1",'',subjects)
            fields_bat,vals_bat=run_query(request.POST.getlist('bat_selections'),"bat",bat_type,subjects)
            fields_img,vals_img=run_query(request.POST.getlist('img_selections'),"img",'',subjects)

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

            subj_data_tuples=list(zip(subjects,vals_day1,vals_bat,vals_img,genos)    )

            if request.POST['action'] == 'Preview':
                #### need to do a bit more research to enable adding the "write csv" button to preview page
                # request.session['context_data'] = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
                # print(request.session['context_data'])
                # print('****0******')
                # request.session.pop('fields',None)
                # request.session['fields']=fields
                return render(request, 'selected_data.html',{'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples})
            else:
                # try:
                #     print('********1*********')
                #     print(fields_day1,subj_data_tuples)
                #     print(request.session['context_data'])
                #     subj_data_tuples,fields,fields_img,fields_day1,fields_bat,fields_snp # check if this is already defined, won't work bc these are defined but empty (excpet subjects)
                #     context_data = {'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}
                # except:
                #     print('********2*********')
                #     context_data = request.session['context_data']  # if not,
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="ExtractedData.csv"'
                t = loader.get_template('write_csv_template.py')
                # response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
                response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
                return response
                # return HttpResponseRedirect("You'd switch to Write CSV mode now.")

        else:
            messages.error(request,"Error", extra_tags='alert')

    else:

        options_img={}
        for fullvar in ImagingVariable.objects.all():
            ## names are in formation task_contrast_ROI.[L/R]
            ### there must be a much more elegant way to do this, but too lazy to figure it out right now
            # if fullvar.var_name[-6:]==".Clust.L" or fullvar.var_name[-6:]==".Clust.R":
            #     var=fullvar.var_name[:-6]
            # elif fullvar.var_name[-4:]==".Vox.L" or fullvar.var_name[-4:]==".Vox.R":
            #     var=fullvar.var_name[:-4]
            if fullvar.var_name[-2:]==".L" or fullvar.var_name[-2:]==".R":
                var=fullvar.var_name[:-2]
            else:
                var=fullvar.var_name
            vargroup=fullvar.vargroup
            if vargroup not in options_img:
                options_img[vargroup]=[]
            if var not in options_img[vargroup]:
                options_img[vargroup].append(var)

        fullnames=[v.var_name.split('_',1)[0] for v in BatteryVariable.objects.all()] # use split to pull only the measure name
        options_bat=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)

        fullnames=[v.var_name.split('_',1)[0] for v in Day1Variable.objects.all()] # use split to pull only the measure name
        options_day1=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)

        form = SelectionForm()
        form_snp = SelectionForm_SNP()
        form_bat_type = SelectionForm_bat_type()

    return render(request, 'select.html',{'form':form,'options_day1':options_day1,'form_bat_type':form_bat_type,'options_bat':options_bat,'options_img':options_img,'form_snp':form_snp})

# def write_csv(request):
#     if request.POST['action'] == 'Write CSV':
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="ExtractedData.csv"'
#         t = loader.get_template('write_csv_template.py')
#         # response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
#         response.write(t.render({'fields':fields,'fields_day1':fields_day1,'fields_bat':fields_bat,'fields_img':fields_img,'fields_snp':fields_snp,'subj_data_tuples':subj_data_tuples}))
#         return response
