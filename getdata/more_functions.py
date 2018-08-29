from .models import BatteryVariable, ImagingVariable, Day1Variable

# Takes the name of an imaging variable in the form of Task_Contrast_ROI
def get_img_subvars(var):
	varlist=[]
	allvars=ImagingVariable.objects.all()
	for v in allvars:
		if v.var_name.startswith(var):
			varlist.append(v.var_name)

	return varlist		

# Takes the name of a battery variable 
def get_bat_subvars(var):
	varlist=[]
	allvars=BatteryVariable.objects.all()
	for v in allvars:
		if v.var_name.startswith(var):
			varlist.append(v.var_name)

	return varlist


# Takes the name of an day1 variable 
def get_day1_subvars(var):
	varlist=[]
	if var == 'CES':
		for i in range(1,8):
			varlist.append('CES'+str(i))
		varlist.append('CES8a')	
		varlist.append('CES8b')
	elif var == 'PCL':
		varlist.append('PCLevent')	
		varlist.append('PCLeventdate')
		for i in range(1,24):
			varlist.append('PCL'+str(i))
	elif var == 'Trails':
		varlist.append('TrailsA_time')
		varlist.append('TrailsA_err')
		varlist.append('TrailsB_time')
		varlist.append('TrailsB_err')
	elif var == 'SDMT':	
		varlist.append(var)
	elif var == 'PASAT':
		varlist.append('PASAT3_raw')	
		varlist.append('PASAT2_raw')
	elif var == 'DigitSpan':
		varlist.append('DS_LDSF')	
		varlist.append('DS_DSFtot')	
		varlist.append('DS_LDSB')	
		varlist.append('DS_LDSBtot')	
		varlist.append('DS_LDSS')	
		varlist.append('DS_DSStot')	
		varlist.append('DS_DS_TOT')	
		varlist.append('DS_DSF_SS')	
		varlist.append('DS_DSB_SS')	
		varlist.append('DS_DSS_SS')	
		varlist.append('DS_DS_TOT_SS')
	elif var == 'CVLT':
		varlist.append('CVLT_Trial1')		
		varlist.append('CVLT_Trial2')		
		varlist.append('CVLT_Trial3')		
		varlist.append('CVLT_Trial4')		
		varlist.append('CVLT_Trial5')		
		varlist.append('CVLT_Trial15')		
		varlist.append('CVLT_TrialB')		
		varlist.append('CVLT_SDFree')		
		varlist.append('CVLT_LDFree')		
	elif var == 'AMNDART':
		varlist.append('AMNART_incorrect')
		varlist.append('AMNART_VIQ')
	elif var == 'WASI':
		varlist.append('WASI_vocab_raw')
		varlist.append('WASI_vocab_T')
		varlist.append('WASI_matrix_raw')
		varlist.append('WASI_matrix_T')
		varlist.append('WASI_FSIQ')
		varlist.append('WASI_FSIQ_percentile')
		varlist.append('WASI_FSIQ_95C')
	elif var == 'VerbalFluency':
		varlist.append('VF_TotF')
		varlist.append('VF_TotA')
		varlist.append('VF_TotS')
		varlist.append('VF_TotAml')
		varlist.append('VF_TotFAS')

	return varlist	
		
