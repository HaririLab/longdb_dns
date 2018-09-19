"""longdb_dns URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from longdb_dns.forms import LoginForm
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView


urlpatterns = [
    path('longdb_dns', TemplateView.as_view(template_name='home.html'),name="home"),
    path('longdb_dns/admin/', admin.site.urls),
    path('longdb_dns/getdata/', include('getdata.urls')),
    path('longdb_dns/checkSNP/', include('checkSNP.urls')),
    path('longdb_dns/stats/', include('stats.urls')),
    path('longdb_dns/iprestrict/', include('iprestrict.urls', namespace='iprestrict')),
    path('longdb_dns/login/', login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login'), # not sure why i had to remove name='login' here???
    path('longdb_dns/logout/', logout, name='logout'),      
]

