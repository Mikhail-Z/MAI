"""hospital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/login/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/logout/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/appointment/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/appointment/submit', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient/my_appointments/', include('hospitalapp.urls', namespace='hospitalapp')),
    url('r^patient/my_appointments/delete/', include('hospitalapp.urls', namespace='hospitalapp')),
    url('r^doctor/login/', include('hospitalapp.urls', namespace='hospitalapp')),

    url(r'^doctor/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/review/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/review/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/review/patient_search/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/issues_history/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/appointment/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/dispanserization/', include('hospitalapp.urls', namespace='hospitalapp')),


    url(r'^doctor/employees_not_found_error/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^doctor/appointment_records/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^check_user/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^logout/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^patient_not_found/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^show_specializations/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^show_appointment_time/', include('hospitalapp.urls', namespace='hospitalapp')),
    url(r'^show_doctors/', include('hospitalapp.urls', namespace='hospitalapp')),
]
