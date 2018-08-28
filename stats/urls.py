from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

app_name = 'stats'

urlpatterns = [
    # ex: /getdata/
    path('', views.stats, name='stats'),
    # ex: /getdata/select/
    #path('select/', views.select, name='select'),
  
    
]
