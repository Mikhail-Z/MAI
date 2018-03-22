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


def create_cardiologist_review_blank(admission_id, text_dict):
    admission_blank = CardiologistAdmissionReview(
        admission_id=admission_id,
        icd10_id=text_dict["icd10_id"],
        complaints=text_dict["complaints"],
        anamnesis=text_dict["anamnesis"],
        survey_data=text_dict["survey_data"],
        general_state=text_dict["general_state"],
        body_temperature=text_dict["body_temperature"],
        bmi=text_dict["BMI"],
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
        d_group=text_dict["D_group"],
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
        instrumental_examinations=text_dict["instrumental_examinations"],
        recommendations=text_dict["recommendations"],
        consultation=text_dict["consultation"],
        medical_therapy=text_dict["medical_therapy"],
        therapy_finished=text_dict["therapy_finished"]
    )
    admission_blank.save()


def create_therapist_dispanserization_blank(admission_id, text_dict):
    print(text_dict)
    admission_blank = TherapistAdmissionDispanserization(
        admission_id=admission_id,
        icd10_id=text_dict["icd10_id"],
        dispanserization_stage=int(text_dict["dispanserization_stage"]),
        complaints=text_dict["complaints"],
        anamnesis=text_dict["anamnesis"],
        general_state=text_dict["general_state"],
        body_temperature=text_dict["body_temperature"],
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
        instrumental_examinations=text_dict["instrumental_examinations"],
        recommendations=text_dict["recommendations"],
        consultation=text_dict["consultation"],
        medical_therapy=text_dict["medical_therapy"],
        preventive_counseling=text_dict["preventive_counseling"],
        spa_treatment=text_dict["spa_treatment"],
        dispansery_status=text_dict["dispansery_status"],
        cardiovascular_risk=text_dict["cardiovascular_risk"],
    )
    admission_blank.save()
