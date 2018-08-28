from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from .models import Day1Variable, BatteryVariable, ImagingVariable, SNP 

class SelectionForm(forms.Form):
	useGender = forms.BooleanField(required=False,label='Gender') #,initial='True'
	useRace = forms.BooleanField(required=False,label='Race')
	useAge = forms.BooleanField(required=False,label='Age')


class SelectionForm_Imaging(forms.Form):
	names=['Hammer_AngerFearGrNeutral_Amunts','Hammer_AngerFearGrNeutral_AALwholeAmygdala',
		'Hammer_AngerFearGrShapes_Amunts','Hammer_AngerFearGrShapes_AALwholeAmygdala',
		'Hammer_Habit1gr2gr3gr4_Amunts','Hammer_Habit1gr2gr3gr4_AALwholeAmygdala',
		'Hammer_FearGrNeutral_Amunts','Hammer_FearGrNeutral_AALwholeAmygdala',
		'Hammer_AngerGrNeutral_Amunts','Hammer_AngerGrNeutral_AALwholeAmygdala',
		'Hammer_SurpriseGrShapes_Amunts','Hammer_SurpriseGrShapes_AALwholeAmygdala',
		'Hammer_NeutralGrShapes_Amunts','Hammer_NeutralGrShapes_AALwholeAmygdala',
		'Hammer_AngerGrShapes_Amunts','Hammer_AngerGrShapes_AALwholeAmygdala',
		'Hammer_FearGrShapes_Amunts','Hammer_FearGrShapes_AALwholeAmygdala',
		'Hammer_FacesGrShapes_Amunts','Hammer_FacesGrShapes_AALwholeAmygdala',
		'Cards_NegGrCtrl_VS','Cards_PosGrCtrl_VS','Cards_PosGrNeg_VS',	
		]
	OPTIONS=zip(names,names)
	imaging_selections = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'size':10,'cols':30}),choices=OPTIONS,required=False,label='')	

class SelectionForm_Battery(forms.Form):
	#names=['']
	names=[v.var_name for v in BatteryVariable.objects.all()]
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