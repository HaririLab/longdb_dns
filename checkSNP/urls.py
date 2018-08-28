from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = 'checkSNP'

urlpatterns = [
    # ex: /getdata/
    path('', views.checkSNP, name='checkSNP'),
    # ex: /getdata/select/
    #path('select/', views.select, name='select'),
  
    
]
