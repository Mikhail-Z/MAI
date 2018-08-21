from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^patient/login/$', views.PatientLoginView.as_view(), name='patient_login'),
    url(r'^patient/logout/$', logout, {"next_page": "/patient/"}),
    url(r'^patient/appointment/$', views.AppointmentView.as_view(), name='appointment'),
    url(r'^patient/appointment/submit/$', views.submit_appointment, name='submit_appointment'),
    url(r'^patient/my_appointments/$', login_required(views.MyFutureAppointmentsView.as_view(), login_url="/patient/login/"), name='my_appointments'),
    url(r'^patient/my_appointments/delete/$', views.delete_appointment, name='delete_appointment'),
    url(r'^doctor/$', views.doctor, name='doctor'),
    url(r'^doctor/login/$', views.DoctorLoginView.as_view(), name='doctor_login'),
    url(r'^doctor/logout/$', logout, {"next_page": "/"}),
    url(r'^doctor/review/$', login_required(views.PatientAdmissionView.as_view(), login_url="/patient/login/"), name="patient_review"),
    url(r'^doctor/review/(?P<admission_id>\d+)', views.review_blank, name="review_blank"),
    url(r'^doctor/review/patient_search/$', views.patient_search, name="patient_search"),
    url(r'^doctor/issues_history/$', views.IssuesHistoryView.as_view(), name="issues_history"),
    url(r'^doctor/appointment/$', views.AppointmentFromDoctorView.as_view(), name="appointment_from_doctor"),
    url(r'^doctor/dispanserization/$', views.DispanserizationStatusView.as_view(), name="dispanserization_status"),
    url(r'^find_icd10/$', views.find_icd10, name="find_icd10"),
]
