from django.contrib.auth.forms import AuthenticationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from django.utils.translation import ugettext_lazy as _, ugettext
from .models import Day1Variable, SNP #BatteryVariable, 

class SelectionForm(forms.Form):
    useGender = forms.BooleanField(required=False,label='Gender') #,initial='True'
    useRace = forms.BooleanField(required=False,label='Ethnicity')
    useAge = forms.BooleanField(required=False,label='Age')


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

class SelectionForm_bat_type(forms.Form):
    useSCORE = forms.BooleanField(required=False,label='Scored',initial='True')
    useREC = forms.BooleanField(required=False,label='Recoded')
    useRAW = forms.BooleanField(required=False,label='Raw')


# # add this to allow bootstrap css
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30,
#                                widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
#     password = forms.CharField(label="Password", max_length=30,
#                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


# class SelectionForm_Imaging(forms.Form):
#     useAmygdala = forms.BooleanField(required=False,label='Amygdala')
#     useVS = forms.BooleanField(required=False,label='VS')
