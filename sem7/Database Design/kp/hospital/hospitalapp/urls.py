from django.conf.urls import url
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('^doctor/$', views.doctor, name='doctor'),
    url(r'^doctor/login/$', views.doctor_login, name='doctor_login'),
    url(r'^doctor/appointment_records/$', views.appointment_records, name='appointment_records'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^patient/login/$', views.patient_login, name='patient_login'),
    url(r'^patient/appointment/$', views.appointment, name='appointment'),
    url(r'^patient_not_found/$', views.patient_not_found, name='patient_not_found'),
    url(r'^patient/my_appointments/$', views.my_appointments, name='my_appointments'),
    url(r'^check_user/', views.check_user_exists, name='check_user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^show_specializations/', views.show_doctor_specialization, name="show_doctor_specialization"),
    url(r'^show_appointment_time/', views.show_appointment_time, name='show_appointment_time'),
    url(r'^show_doctors/', views.show_doctors, name='show_doctors'),
]

'''
url('^doctor/appointment_records/$', name='appointment_records'),
url('^doctor/$', views.doctor, name='doctor'),
'''


'''
    url('^$', views.index, name='index'),
    url('^doctor/$', views.doctor, name='doctor'),
    url('^patient/$', views.patient, name='patient'),
    url('^doctor/signin$', views.doctor_signin, name='doctor_signin'),
    # url('^doctor/signup$', views.doctor_signup, name='doctor_signup'),
    url('^patient/signin$', views.patient_signin, name='patient_signin'),
    url('^patient/signup$', views.patient_signup, name='patient_signup'),
    url('^patient/admission$', views.patient_admission, name='patient_admission'),
    url('^patient/appointment$', views.patient_appointment, name='patient_appointment'),
    '''