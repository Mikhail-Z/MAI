from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from ..models import *
from django.db import connection
from django.db.models import Q
import psycopg2

import datetime
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from .help_functions import *


class PatientLoginView(View):

    def get(self, request):
        request.session["redirect_url"] = request.GET.get("next")
        return render(request, "hospitalapp/patient_login.html")

    def post(self, request):
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_url = request.session.pop("redirect_url")
            if redirect_url is None:
                redirect_url = "/patient/"
            return HttpResponseRedirect(redirect_url)
        else:
            return render(request, "hospitalapp/patient_login.html", context={"after_wrong_login": True})


def patient(request):
    return render(request, 'hospitalapp/patient.html')


class MyFutureAppointmentsView(View):
    template_name = "hospitalapp/my_appointments.html"

    def get(self, request, **kwargs):
        cur_patient_info = self._get_current_patient_info(request)[0]
        future_appointments = self._get_future_appointments(cur_patient_info["id"])
        page = request.GET.get('page')
        appointments_per_page = 5
        paginator = Paginator(future_appointments, appointments_per_page)
        try:
            appointments_on_cur_page = paginator.page(page)
        except PageNotAnInteger:
            appointments_on_cur_page = paginator.page(1)
        except EmptyPage:
            appointments_on_cur_page = paginator.page(paginator.num_pages)

        return render(request, self.template_name,
                      context={
                          "appointments": appointments_on_cur_page,
                          "patient_info": cur_patient_info,
                      })

    def _get_current_patient_info(self, request):
        cursor = connection.cursor()
        query = "select id, last_name, INITCAP(first_name) as first_name, INITCAP(patronymic) as patronymic " \
                "from patient P WHERE P.user_id = %s"
        cursor.execute(query, [request.user.id])
        return dictfetchall(cursor)

    def _get_future_appointments(self, patient_id):
        cursor = connection.cursor()
        query = """select pa.id as id, d.last_name as doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic,
                 s.specialization_name as doctor_specialization, pa.appointment_datetime as appointment_datetime, c.number as cabinet_number
                 from patients_appointment_to_doctors pa        
                 join doctor_specialization ds on (ds.id = pa.doctor_specialization_id)
                 JOIN cabinet c on (pa.cabinet_id = c.id)
                 join doctor d on (d.id = ds.doctor_id)
                 join specialization s on (s.id = ds.specialization_id)
                 where (pa.appointment_datetime > now() and pa.free = 'f' and pa.patient_id = %s);"""
        cursor.execute(query, [patient_id])
        return dictfetchall(cursor)


@login_required(login_url="/patient/login/")
def delete_appointment(request):
    if request.method == "POST":
        appointment_id = request.POST.get("appointment_id", None)
        if appointment_id:
            update_rows_num = PatientsAppointmentToDoctors.objects.\
                filter(id=appointment_id).update(free='f', patient_id=None)
            return redirect("hospitalapp:my_appointments")
    else:
        return HttpResponse(
            content={"message": "only POST method is allowed"},
            status=405
        )


@login_required(login_url="/patient/login/")
def submit_appointment(request):
    if request.method == "POST":
        appointment_id = request.session.get("appointment_id", None)
        patient_id = Patient.objects.get(user_id=int(request.user.id)).id
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
                    request, "hospitalapp/appointment_result.html",
                    context={
                        "appointment_result_msg": "Не удалось записаться."
                                                  " Возможно, на это время уже есть запись."
                                                  " Попробуйте заново на другое время."
                    })
    else:
        appointment_id = request.GET.get("appointment_id", None)
        print("appintment id:", appointment_id)
        if appointment_id:
            request.session["appointment_id"] = appointment_id
        query = """select d.last_name as doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic,
                  pa.appointment_datetime as appointment_datetime, c.number as cabinet_number, s.specialization_name as specialization_name from 
                  patients_appointment_to_doctors pa JOIN
                  doctor_specialization ds  on (ds.id = pa.doctor_specialization_id) join
                  specialization s on (s.id= ds.specialization_id) join
                  cabinet c on (c.id = pa.cabinet_id) JOIN 
                  doctor d on (d.id = ds.doctor_id)
                  where (pa.id = %s)"""
        cursor = connection.cursor()
        cursor.execute(query, [int(appointment_id)])
        future_appointment_info = dictfetchall(cursor)[0]
        return render(request, "hospitalapp/submit_appointment.html", context={"appointment_info": future_appointment_info})


class AppointmentView(View):
    template_name = "hospitalapp/appointment.html"

    def get(self, request) -> JsonResponse:
        if request.GET.get("date", None):
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
            DoctorSpecialization.objects.values("specialization__id", "specialization__specialization_name").filter(specialization__is_hidden=False)
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
        date_str = request.GET["date"]
        doctor_id = request.session["doctor_id"]
        specialization_id = request.session["specialization_id"]
        date = datetime.datetime.strptime(date_str, "%d.%m.%Y")

        cursor = connection.cursor()
        query = "select pa.id, pa.free, to_char(pa.appointment_datetime, 'HH24:MI')" \
                " from patients_appointment_to_doctors pa"  \
                " join doctor_specialization ds on (pa.doctor_specialization_id = ds.id)" \
                " where (ds.doctor_id = %s and ds.specialization_id = %s and" \
                " pa.appointment_datetime::date = %s and pa.appointment_datetime > now())" \
                " ORDER by to_char(pa.appointment_datetime, 'HH24:MI')"
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