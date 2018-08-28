from django.contrib import admin
from .models import Subject, ChromosomeID, TypedSNP, ImagingValue, BatteryValue, Genotype,SNP,ImagingVariable,BatteryVariable,Day1Value,Day1Variable

admin.site.register(Subject)
admin.site.register(BatteryValue)
admin.site.register(BatteryVariable)
admin.site.register(ImagingValue)
admin.site.register(ImagingVariable)
admin.site.register(Day1Value)
admin.site.register(Day1Variable)
admin.site.register(Genotype)
admin.site.register(SNP)
