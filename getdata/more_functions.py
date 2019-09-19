from .models import FreeSurferVariable, FreeSurferValue, BatteryVariable, ImagingVariable, Day1Variable, ImagingValue, BatteryValue, Day1Value, CompositeVariable, CompositeValue
from django.db.models import Q, Prefetch
from functools import reduce

### edited to include different batvar types (RAW, REC) and remove var_type overlap with BatteryVariable field
# Takes the name of an imaging variable in the form of Task_Contrast_ROI
def get_subvars(var,var_cat,bat_type):
    if var_cat == "freesurfer":
        allvars=FreeSurferVariable.objects.all()
    elif var_cat == "bat":
        if not bat_type:
            allvars=BatteryVariable.objects.all()
        else:
            allvars=BatteryVariable.objects.filter(var_type__in=bat_type)
    elif var_cat == "day1":
        allvars=Day1Variable.objects.all()
    elif var_cat == "comp":
        allvars=CompositeVariable.objects.all()    
    else:
        print("Invalid var_cat: "+var_cat)
        return
    varlist=[]
    for v in allvars:
        if var=="ALL_REGIONS" or v.var_name.startswith(var):
            varlist.append(v.var_name)
    return varlist

def run_query(requested_vars,var_cat,bat_type,subjects): # bat_type here refers to a list of BatteryVariable.var_type selected by user
    if var_cat == "freesurfer":
        allvars=FreeSurferVariable.objects
        allvals=FreeSurferValue.objects
    elif var_cat == "bat":
        allvars=BatteryVariable.objects
        allvals=BatteryValue.objects
    elif var_cat == "day1":
        allvars=Day1Variable.objects
        allvals=Day1Value.objects
    elif var_cat == "comp":
        allvars=CompositeVariable.objects
        allvals=CompositeValue.objects      
    else:
        print("Invalid var_cat: "+var_cat)
        return
    related_name=var_cat+'val'
    vars_out=[]
    fields_out=[]
    for requested_var in requested_vars:
        for subvar in get_subvars(requested_var,var_cat,bat_type):
            vars_out.append(allvars.get(var_name=subvar))
            fields_out.append(subvar)
    if(len(vars_out)>0):
        subjects_out=subjects.prefetch_related(  # filter(gender='F').
            Prefetch(
                    related_name,
                    queryset=allvals.filter(reduce(lambda x, y: x | y, [Q(variable=v) for v in vars_out])),
                    to_attr='fetched_vals'
            )
        )
        ## original solution - doesn't work since fetched variables aren't always in the same order!!
        # subjects_out = list(subjects_out)
        # indices=[fields_out.index(subjects_out[0].fetched_vals[i].variable_id) for i in range(0,len(fields_out))]  #### if this isn't working, it might be because the first subject does not have values for the given variable, and you need to create null ones!
        # indices_rev=[indices.index(i) for i in range(0, len(indices))]
        # vals_out=[[s.fetched_vals[i] if i < len(s.fetched_vals) else None for i in indices_rev] for s in subjects_out] ###### this line changes the order of s.fetched_vals if more than one con_ROI is selected!!!!!
        ## new solution!!
        vals_out=[]
        for s in list(subjects_out):
            this_subjects_vars=[]
            for i in range(0,len(fields_out)):
                cur_var=next(filter(lambda x: x.variable_id==fields_out[i], s.fetched_vals))
                if cur_var is None:
                    this_subjects_vars.append(None)
                else:
                    this_subjects_vars.append(cur_var)
            vals_out.append(this_subjects_vars)
    else:
        vals_out=[[] for s in subjects] # need this for zip to work later
    return fields_out,vals_out










# # Takes the name of an day1 variable
# def get_day1_subvars(var):
#     varlist=[]
#     if var == 'CES':
#         for i in range(1,8):
#             varlist.append('CES'+str(i))
#         varlist.append('CES8a')
#         varlist.append('CES8b')
#     elif var == 'PCL':
#         varlist.append('PCLevent')
#         varlist.append('PCLeventdate')
#         for i in range(1,24):
#             varlist.append('PCL'+str(i))
#     elif var == 'Trails':
#         varlist.append('TrailsA_time')
#         varlist.append('TrailsA_err')
#         varlist.append('TrailsB_time')
#         varlist.append('TrailsB_err')
#     elif var == 'SDMT':
#         varlist.append(var)
#     elif var == 'PASAT':
#         varlist.append('PASAT3_raw')
#         varlist.append('PASAT2_raw')
#     elif var == 'DigitSpan':
#         varlist.append('DS_LDSF')
#         varlist.append('DS_DSFtot')
#         varlist.append('DS_LDSB')
#         varlist.append('DS_LDSBtot')
#         varlist.append('DS_LDSS')
#         varlist.append('DS_DSStot')
#         varlist.append('DS_DS_TOT')
#         varlist.append('DS_DSF_SS')
#         varlist.append('DS_DSB_SS')
#         varlist.append('DS_DSS_SS')
#         varlist.append('DS_DS_TOT_SS')
#     elif var == 'CVLT':
#         varlist.append('CVLT_Trial1')
#         varlist.append('CVLT_Trial2')
#         varlist.append('CVLT_Trial3')
#         varlist.append('CVLT_Trial4')
#         varlist.append('CVLT_Trial5')
#         varlist.append('CVLT_Trial15')
#         varlist.append('CVLT_TrialB')
#         varlist.append('CVLT_SDFree')
#         varlist.append('CVLT_LDFree')
#     elif var == 'AMNDART':
#         varlist.append('AMNART_incorrect')
#         varlist.append('AMNART_VIQ')
#     elif var == 'WASI':
#         varlist.append('WASI_vocab_raw')
#         varlist.append('WASI_vocab_T')
#         varlist.append('WASI_matrix_raw')
#         varlist.append('WASI_matrix_T')
#         varlist.append('WASI_FSIQ')
#         varlist.append('WASI_FSIQ_percentile')
#         varlist.append('WASI_FSIQ_95C')
#     elif var == 'VerbalFluency':
#         varlist.append('VF_TotF')
#         varlist.append('VF_TotA')
#         varlist.append('VF_TotS')
#         varlist.append('VF_TotAml')
#         varlist.append('VF_TotFAS')

#     return varlist
