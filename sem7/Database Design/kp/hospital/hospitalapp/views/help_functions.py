from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.core.exceptions import ObjectDoesNotExist
from collections import defaultdict
from django.core.cache import cache
from django.utils import timezone
from django.db import IntegrityError, transaction
import pytz
from ..models import *
from django.db import connection
from django.db.models import Q
import psycopg2

import datetime
import json
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
import smtplib

def check_user_exists(request):
    login = request.GET.get('login')
    password = request.GET.get('password')
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


import smtplib


class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, email_to, subject, body):
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + email_to,
            "MIME-Version: 1.0",
            "Content-Type: text/html"
        ]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            self.email,
            headers + "\r\n\r\n" + body
        )

from email.mime.text import MIMEText
from email.header import Header


def send_email(email_from, email_to, full_name):
    password = "need4you"
    body = """
    Здравствуйте, {}.\nНапоминаем Вам, что в этом году Вы можете бесплатно пройти плановую диспансеризацию в поликлиинке №14 по адресу г. Рязань, ул. Семинарская, д. 46, кабинет №23 (медицинской профилактики) с 08:00 до 19:00.

    Скрининг позволяет выявлять заболевания в их ранних, бессимптомных стадиях, на которых лечение более эффективно.
    """.format(full_name)


    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header("Диспансеризация", "utf-8")
    msg["From"] = email_from
    msg["To"] = email_to
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.ehlo()
        server.starttls()
        server.login(email_from, password)
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
    finally:
        server.quit()
# send_email("mike.rzn@gmail.com", "mike.rzn@yandex.ru", "Михаил Константинович")

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def handle_input_text(text_dict):
    res_text_dict = {}
    for title in text_dict:
        res_text = re.sub(r"([ ]+|\t+)", r" ", text_dict[title])
        res_text = res_text.strip().replace("\r\n", "")
        res_text_dict[title] = res_text
    return res_text_dict


def get_appointment_info(appointment_id):
    return PatientsAppointmentToDoctors.objects.filter(
        id=appointment_id).values(
        "id", "doctor_specialization__doctor__last_name",
        "doctor_specialization__doctor__first_name",
        "doctor_specialization__doctor__patronymic",
        "doctor_specialization__specialization__specialization_name",
        "appointment_datetime",
        "cabinet__number"
    )


def find_icd10(request):
    cursor = connection.cursor()
    pattern = "{}{}{}".format("%", request.GET.get("icd10_text"), "%")
    query = "select id, code, name from icd10 where (upper(code || name) like upper(%s))"
    cursor.execute(query, [pattern])
    icd10_issues = cursor.fetchall()
    return JsonResponse(icd10_issues, safe=False)


def get_number_if_numeric(s, type2transform):
    if s.isnumeric():
        return type2transform(s)


def get_cursor_with_query_for_dispanserization_in_this_year(table_name):
    cursor = connection.cursor()
    query = """select pa.id as admission_id, p.last_name as patient_last_name, p.first_name as patient_first_name, p.patronymic as patient_patronymic,
                          p.date_birth as patient_date_birth, pa.admission_datetime::date as admission_date, sat.health_group
                          dispansery_status.name as dispansery_status, sat.dispanserization_stage as dispanserization_stage, sat.dispanserization_finished 
                          from {specialist_admission_table} sat join patients_admission_to_doctors pa on (sat.admission_id = pa.id)
                          JOIN patient p on (p.id = pa.patient_id)
                          left join dispansery_status on (dispansery_status.id = sat.dispansery_status_id)
                          where (extract(year from now()) - extract(YEAR FROM p.date_birth)) >= 21 and (extract(year from now()) - extract(YEAR FROM p.date_birth))::int % 3 = 0 
                       """.format(specialist_admission_table=table_name[0])
    return cursor


def create_cardiologist_review_blank(admission_id, text_dict):
    admission_blank = CardiologistAdmissionReview(
        admission_id=admission_id,
        icd10_id=text_dict["icd10_id"],
        complaints=text_dict["complaints"],
        anamnesis=text_dict["anamnesis"],
        survey_data=text_dict["survey_data"],
        general_state=text_dict["general_state"],
        body_temperature=text_dict["body_temperature"],
        height=get_number_if_numeric(text_dict["height"], float),
        weight=get_number_if_numeric(text_dict["weight"], float),
        bmi=get_number_if_numeric(text_dict["bmi"], float),
        consciousness=text_dict["consciousness"],
        skin_integument=text_dict["skin_integument"],
        turgor_reduced=text_dict["turgor_reduced"],
        visible_mucous=text_dict["visible_mucous"],
        lungs=text_dict["lungs"],
        percutary_sound=text_dict["percutary_sound"],
        respiratory_noise=text_dict["respiratory_noise"],
        wheezing=text_dict["wheezing"],
        pulse=text_dict["pulse"],
        filling=text_dict["filling"],
        pulse_deficit=text_dict["pulse_deficit"],
        pressure=text_dict["pressure"],
        obtuse_boundaries=text_dict["obtuse_boundaries"],
        heart_tones=text_dict["heart_tones"],
        liver=text_dict["liver"],
        liver_edge=text_dict["liver_edge"],
        urination=text_dict["urination"],
        edema=text_dict["edema"],
        additional_information=text_dict["additional_information"],
        appointments=text_dict["appointments"],
        drugs=text_dict["drugs"],
        therapy_finished=handle_input_text["therapy_finished"]
    )
    admission_blank.save()


def create_therapist_review_blank(admission_id, text_dict):
    admission_blank = TherapistAdmissionReview(
        admission_id=admission_id,
        icd10_id=text_dict["icd10_id"],
        complaints=text_dict["complaints"],
        anamnesis=text_dict["anamnesis"],
        general_state=text_dict["general_state"],
        body_temperature=text_dict["body_temperature"],
        height=get_number_if_numeric(text_dict["height"], float),
        weight=get_number_if_numeric(text_dict["weight"], float),
        rashes=text_dict["rashes"],
        humidity=text_dict["humidity"],
        wheezing=text_dict["wheezing"],
        peripheral_lymph_nodes=text_dict["peripheral_lymph_nodes"],
        pastosity=text_dict["pastosity"],
        nose_breath=text_dict["nose_breath"],
        respiratory_rate=text_dict["respiratory_rate"],
        lungs_breathe=text_dict["lungs_breathe"],
        heart_tones=text_dict["heart_tones"],
        heart_noise=text_dict["heart_noise"],
        heart_rate=text_dict["heart_rate"],
        pressure=text_dict["pressure"],
        tongue=text_dict["tongue"],
        yawn=text_dict["yawn"],
        stomach=text_dict["stomach"],
        liver=text_dict["liver"],
        spleen=text_dict["spleen"],
        amygdala=text_dict["amygdala"],
        urination=text_dict["urination"],
        chair=text_dict["chair"],
        joints_movement=text_dict["joints_movement"],
        assigned_analyzes=text_dict["assigned_analyzes"],
        consultation=text_dict["consultation"],
        medical_therapy=text_dict["medical_therapy"],
        therapy_finished=text_dict["therapy_finished"],
        additional_details=text_dict["additional_details"],
        bmi=get_number_if_numeric(text_dict["bmi"], float)
    )
    admission_blank.save()


def create_therapist_dispanserization_blank(admission_id, text_dict):
    admission_blank = TherapistAdmissionDispanserization(
        admission_id=admission_id,
        icd10_id=text_dict["icd10_id"],
        dispanserization_stage=text_dict["dispanserization_stage"],
        complaints=text_dict["complaints"],
        anamnesis=text_dict["anamnesis"],
        general_state=text_dict["general_state"],
        body_temperature=text_dict["body_temperature"],
        height=get_number_if_numeric(text_dict["height"], float),
        weight=get_number_if_numeric(text_dict["weight"], float),
        bmi=get_number_if_numeric(text_dict["bmi"], float),
        rashes=text_dict["rashes"],
        humidity=text_dict["humidity"],
        wheezing=text_dict["wheezing"],
        peripheral_lymph_nodes=text_dict["peripheral_lymph_nodes"],
        pastosity=text_dict["pastosity"],
        nose_breath=text_dict["nose_breath"],
        respiratory_rate=text_dict["respiratory_rate"],
        lungs_breathe=text_dict["lungs_breathe"],
        heart_tones=text_dict["heart_tones"],
        heart_noise=text_dict["heart_noise"],
        heart_rate=text_dict["heart_rate"],
        pressure=text_dict["pressure"],
        tongue=text_dict["tongue"],
        yawn=text_dict["yawn"],
        stomach=text_dict["stomach"],
        liver=text_dict["liver"],
        spleen=text_dict["spleen"],
        amygdala=text_dict["amygdala"],
        urination=text_dict["urination"],
        chair=text_dict["chair"],
        joints_movement=text_dict["joints_movement"],
        assigned_analyzes=text_dict["assigned_analyzes"],
        recommendations=text_dict["recommendations"],
        consultation=text_dict["consultation"],
        medical_therapy=text_dict["medical_therapy"],
        preventive_counseling=text_dict["preventive_counseling"],
        spa_treatment=text_dict["spa_treatment"],
        dispansery_status=text_dict["dispansery_status"],
        cardiovascular_risk=text_dict["cardiovascular_risk"],
        additional_details=text_dict["additional_details"],
        health_group=text_dict["health_group"],
    )
    admission_blank.save()


def create_general_prevention_dispanserization_blank(admission_id, text_dict):
    admission_blank = GeneralPreventionDispanserizationBlank(
        dispanserization_stage=text_dict["dispanserization_stage"],
        admission_id=admission_id,
        height=get_number_if_numeric(text_dict["height"], float),
        weight=get_number_if_numeric(text_dict["weight"], float),
        bmi=get_number_if_numeric(text_dict["bmi"], float),
        arterial_pressure=text_dict["arterial_pressure"],
        eye_pressure=text_dict["eye_pressure"]
    )
    admission_blank.save()