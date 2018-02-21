from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db import IntegrityError, transaction
import pytz
from django.core import serializers
from .forms import LoginForm
from .models import *

from django.db import connection
import psycopg2
from .models import *
import datetime
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'GET':
        afterRequest = request.GET.get('afterAction', None)
        print("after request", afterRequest, request.is_ajax())
        if afterRequest:
            return JsonResponse({'redirect': reverse('hospitalapp:index')})
        else:
            return render(request, 'hospitalapp/index.html')


def doctor(request):
    if request.user.is_authenticated():
        url = 'hospitalapp:appointment_records'
        return HttpResponseRedirect(reverse(url))
    else:
        url = 'hospitalapp:doctor_login'
        return HttpResponseRedirect(reverse(url))


def patient_not_found(request):
    print('in patient_not_found')
    return render(request, "hospitalapp/patient_not_found.html")


class PatientLoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "hospitalapp/login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        appointment_id = request.POST.get('appointment_id', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.session.get("appointment_id", None):
                appointment_id = request.session["appointment_id"]
                appointment_info = get_appointment_info(appointment_id)
                return render(request, "hospitalapp/submit_appointment.html",
                              context={"appointment_info": appointment_info[0]})
        else:
            return render(request, "hospitalapp/login.html", context={"after_wrong_login": True, "appointment_id": appointment_id})


def patient_login_method_choice(request):
    appointment_id = request.GET.get("appointment_id", None)
    if appointment_id:
        request.session["appointment_id"] = appointment_id
    return render(request, "hospitalapp/login.html")


def check_user_exists(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
    print("login: ", login)
    print("password:", password)
    user = authenticate(username=login, password=password)
    if user is not None:
        login(request, user)
        url = 'hospitalapp:appointment'
        return JsonResponse({
            'success': True,
            'url': reverse(url)
        })
    else:
        return JsonResponse({'success': False})


def my_appointments(request):
    # cursor = connection.cursor()
    # cursor.execute("select DS.specialization_name, E.last_name, E.first_name, E.patronymic, PA.appointment_time"
    #                " from patients_appointment PA join employee E using(employee_id)"
    #                " join Doctor_Specialization DS using(specialization_id)"
    #                " where PA.patient_id = %s and PA.free = 'f'"
    #                " order by PA.appointment_time desc", [request.user.doctor_id,])
    # page = request.GET.get('page')
    # appointments_list = cursor.fetchall()
    # paginator = Paginator(appointments_list, 5)
    # try:
    #     cur_appointments = paginator.page(page)
    # except PageNotAnInteger:
    #     cur_appointments = paginator.page(1)
    #     print(cur_appointments)
    # except EmptyPage:
    #     cur_appointments = paginator.page(paginator.num_pages)
    return render(request, 'hospitalapp/my_appointments.html')


def patient(request):
    if request.method == "GET":
        if request.GET.get("afterLogin", None):
            url = "hospitalapp:patient"
            return HttpResponseRedirect(reverse(url))
        my_appointments_url = reverse('hospitalapp:my_appointments')
        return render(request, 'hospitalapp/patient.html', {'my_appointments_url': my_appointments_url})
    else:
        url = 'hospitalapp:patient_login'
        return HttpResponseRedirect(reverse(url))


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def show_doctor_specialization(request):
    doctor_specializations = list(DoctorSpecialization.objects.order_by('specialization_name').distinct().values())
    print(doctor_specializations)
    if request.is_ajax():
        json = {'specializations': doctor_specializations}
        return JsonResponse(json)
    else:
        return render(request, 'hospitalapp/appointment.html', {'doctor_specializations': doctor_specializations})


def show_appointment_time(request):
    print('in appointment_time')
    specialization_id = request.GET.get('specialization_id', None)
    print(specialization_id)
    if specialization_id is None:
        return appointment(request)
    else:
        free_appointment_time = list(PatientsAppointment.objects.order_by('appointment_time').\
            filter(appointment_time__gt=datetime.datetime.now(), free=True,
                   employee__specialization_id=specialization_id).distinct().values('appointment_time'))
    return HttpResponse(json.dumps(free_appointment_time, default=datetime_handler), content_type='application/json')


def show_doctors(request):
    specialization_id = request.GET.get('specialization_id', None)
    appointment_time = request.GET.get('appointment_time', None)
    print(specialization_id, appointment_time)

    '''appointment_time = datetime.datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M:%S')
    #appointment_time = timezone.localtime(appointment_time, 'Europe/Moscow')
    tz = pytz.timezone('Europe/Moscow')
    appointment_time = tz.localize(appointment_time)
    print(appointment_time.strftime('%Y-%m-%d %H:%M:%S%z'))'''
    if specialization_id and appointment_time:
        cursor = connection.cursor()
        cursor.execute(
            "select PA.appointment_id, E.last_name, E.first_name, E.patronymic from patients_appointment PA "
            "join employee E using (employee_id) where (appointment_time = %s and E.specialization_id = %s);",
            [appointment_time, specialization_id])
        cols = ('doctor_id', 'last_name', 'first_name', 'patronymic')
        doctors = [dict(zip(cols, doctor_info)) for doctor_info in cursor.fetchall()]
        return JsonResponse(doctors, safe=False)
    else:
        return appointment(request)


def appointment(request):
    appointment_id = request.GET.get('appointment_id', None)
    print(appointment_id)
    if appointment_id:
        updated_row = PatientsAppointment.objects.select_for_update().filter(pk=appointment_id, free=True).update(
            patient_id=request.user.id,
            free=False)
        print("updated_row:", updated_row)
        if updated_row > 0:
            return HttpResponse('Yes')
        else:
            return HttpResponse('No')
    return show_doctor_specialization(request)


def appointment_records(request):
    cursor = connection.cursor()
    cursor.execute('select P.first_name, P.last_name, PA.appointment_time from '
                  'patients_appointment PA join patient P on PA.patient_id = P.patient_id '
                  'join employee E on E.employee_id = PA.employee_id '
                  'where E.joining_staff = True and E.user_id = %s and PA.free = True '
                   'and date(PA.appointment_time) = %s;', [request.user.id, datetime.date(2017, 12, 15)])
    col_names = ['First name', 'Last name', 'Time']
    appointments = cursor.fetchall()
    return render(request, 'hospitalapp/patients_appointment.html', {'appointments': appointments,
                                                                      'col_names': col_names})


class AppointmentView(View):
    template_name = "hospitalapp/appointment.html"

    def get(self, request):
        if request.GET.get("time", None):
            print("time")
        elif request.GET.get("date", None):
            request.session["date"] = request.GET["date"]
            return self._show_times(request)
        elif request.GET.get("doctor", None):
            request.session["doctor_id"] = request.GET["doctor"]
            return self._show_dates(request)
        elif request.GET.get("specialization", None):
            request.session["specialization_id"] = request.GET["specialization"]
            return self._show_doctors(request)
        else:
            return self._show_specializations(request)

    def _show_specializations(self, request):
        doctor_specializations = list(
            DoctorSpecialization.objects.values("specialization__id", "specialization__specialization_name").distinct()
        )
        print(doctor_specializations)
        return render(request, self.template_name,
                      {'doctor_specializations': doctor_specializations})

    def _show_doctors(self, request):
        doctor_specialization = request.session["specialization_id"]
        doctors = list(
            DoctorSpecialization.objects.filter(specialization_id=doctor_specialization).order_by(
                "doctor__last_name", "doctor__first_name", "doctor__patronymic"
            ).values("doctor__last_name", "doctor__first_name", "doctor__patronymic", "doctor__id")
        )
        return JsonResponse(doctors, safe=False)

    def _show_dates(self, request):
        doctor_id = request.GET["doctor"]
        specialization_id = request.session["specialization_id"]
        cursor = connection.cursor()
        query = "select distinct(appointment_datetime::date) from patients_appointment_to_doctors pa" \
        " join doctor_specialization ds on (pa.doctor_specialization_id = ds.id)" \
                " where (appointment_datetime > now() and ds.specialization_id = %s and ds.doctor_id = %s);"
        cursor.execute(query, [specialization_id, doctor_id])
        appointment_dates = cursor.fetchall()

        dates_and_weekdays = [d[0].strftime("%d.%m.%Y %w").split(" ") for d in appointment_dates]
        dates_and_weekdays_in_russian = self._change_english_weekdays2russian(dates_and_weekdays)
        dates_and_weekdays_in_russian_dict = self._make_date_and_weekdays_dict_from_pair(dates_and_weekdays_in_russian)
        return JsonResponse(dates_and_weekdays_in_russian_dict, safe=False)

    def _show_times(self, request):
        print(request.GET)
        date_str = request.GET["date"]
        doctor_id = request.session["doctor_id"]
        specialization_id = request.session["specialization_id"]
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")

        cursor = connection.cursor()
        query = "select pa.id, pa.free, to_char(pa.appointment_datetime, 'HH:MI')" \
                " from patients_appointment_to_doctors pa"  \
                " join doctor_specialization ds on (pa.doctor_specialization_id = ds.id)" \
                " where (ds.doctor_id = %s and ds.specialization_id = %s and" \
                " pa.appointment_datetime::date = %s and pa.appointment_datetime > now());"
        cursor.execute(query, [doctor_id, specialization_id, date])
        appointments_info = cursor.fetchall()
        print(appointments_info)
        appointments_info_dict = self._make_dict_from_appointments_info(appointments_info)
        return JsonResponse(appointments_info_dict, safe=False)

    @staticmethod
    def _change_english_weekdays2russian(dates_and_weekdays):
        weekdays_dict = {
            "1": "Понедельник",
            "2": "Вторник",
            "3": "Среда",
            "4": "Четверг",
            "5": "Пятница",
            "6": "Суббота",
            "7": "Воскресенье"
        }
        return [(date_and_weekday[0], weekdays_dict.get(date_and_weekday[1]))
                for date_and_weekday in dates_and_weekdays]

    @staticmethod
    def _make_date_and_weekdays_dict_from_pair(dates_and_weekdays):
        return [{"date": date_and_weekday[0], "weekday": date_and_weekday[1]}
                for date_and_weekday in dates_and_weekdays]

    @staticmethod
    def _make_dict_from_appointments_info(appointments_info):
        return [
            {
                "id": appointment_info[0],
                "free": appointment_info[1],
                "time": appointment_info[2]
            } for appointment_info in appointments_info
        ]


def submit_appointment(request):
    if request.method == "POST":
        appointment_id = request.session.get("appointment_id", None)
        patient_id = list(Patient.objects.filter(user_id=request.user.id).values_list("id"))[0][0]
        if appointment_id:
            updates_rows_num = PatientsAppointmentToDoctors.objects.\
                filter(id=appointment_id, free='t').update(free='f', patient_id=patient_id)
            logout(request)
            if updates_rows_num:
                return render(
                    request, "hospitalapp/appointment_result.html",
                    context={"appointment_result_msg": "Вы успешно записались к специалисту."}
                )
            else:
                return render(
                    request, "/hospitalapp/appointment_result.html",
                    context={
                        "appointment_result_msg": "Не удалось записаться."
                                                  " Возможно, на это время уже есть запись."
                                                  " Попробуйте заново на новое время."
                    })
    else:
        return render(
            request, "hospitalapp/appointment_result.html",
            context={
                "appointment_result_msg": "Вы успешно записались к специалисту."
            }
        )


def get_appointment_info(appointment_id):
        return PatientsAppointmentToDoctors.objects.filter(id=appointment_id).\
            values("id", "doctor_specialization__doctor__last_name",
                   "doctor_specialization__doctor__first_name",
                   "doctor_specialization__doctor__patronymic",
                   "doctor_specialization__specialization__specialization_name",
                   "appointment_datetime",
                   "cabinet__number")