from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from .models import SNP, BatteryVariable, Day1Variable, ImagingVariable

class SelectionForm(forms.Form):
	useGender = forms.BooleanField(required=False,label='Gender') #,initial='True'
	useRace = forms.BooleanField(required=False,label='Race')
	useAge = forms.BooleanField(required=False,label='Age')


class SelectionForm_Imaging(forms.Form):
	fullnames=[v.var_name.split('_',2)[0]+'_'+v.var_name.split('_',2)[1] for v in ImagingVariable.objects.all()] # use split to pull only the measure name
	names=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)
	OPTIONS=zip(names,names)
	imaging_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':30}),choices=OPTIONS,required=False,label='')	

class SelectionForm_Battery(forms.Form):
	fullnames=[v.var_name.split('_',1)[0] for v in BatteryVariable.objects.all()] # use split to pull only the measure name
	names=sorted(set(fullnames)) # get unique entries (i.e. one for each measure)
	OPTIONS=zip(names,names)
	battery_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':15}),choices=OPTIONS,required=False,label='')	

class SelectionForm_Day1(forms.Form):
	names=['CES','PCL','Trails','SDMT','PASAT','DigitSpan','CVLT','AMNART','WASI','VerbalFluency']
	OPTIONS=zip(names,names)
	day1_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':15}),choices=OPTIONS,required=False,label='')	

class SelectionForm_SNP(forms.Form):
	rsIDs = forms.CharField(widget=forms.Textarea(attrs={'rows':10,'cols':25}),label='',required=False) #widget=forms.Textarea,

	def clean_rsIDs(self):
		input_rsIDs = self.cleaned_data['rsIDs'].splitlines()
		for i in input_rsIDs:
			try: 
				snp = SNP.objects.get(rs_id=i)
			except SNP.DoesNotExist:
				raise forms.ValidationError(('%(rsID)s is not genotyped in DNS. Check imputed data.'),code='doesnotexist',params={'rsID':i},)
		return input_rsIDs

# # add this to allow bootstrap css
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30, 
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
#     password = forms.CharField(label="Password", max_length=30, 
#                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


# class SelectionForm_Imaging(forms.Form):
# 	useAmygdala = forms.BooleanField(required=False,label='Amygdala')
# 	useVS = forms.BooleanField(required=False,label='VS')