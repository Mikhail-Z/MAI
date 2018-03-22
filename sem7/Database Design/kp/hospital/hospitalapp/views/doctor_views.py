from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
import re
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from collections import defaultdict
from django.core.cache import cache
from ..models import *
from django.db import connection
from django.db.models import Q
import psycopg2
from .help_functions import *
import datetime
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


@login_required(login_url="/patient/login/")
def doctor(request):
    if request.is_ajax():
        specialization_name = request.GET.get("specialization_name")
        specialization_id = request.GET.get("specialization_id")
        if specialization_name and specialization_id:
            doctor_id = request.session["cur_doctor_id"]
            doctor_specialization_id = DoctorSpecialization.objects.get(
                specialization_id=specialization_id,
                doctor_id=doctor_id
            ).id
            request.session["cur_specialization_id"] = specialization_id
            request.session["cur_specialization_name"] = specialization_name
            request.session["cur_doctor_specialization_id"] = doctor_specialization_id
        return HttpResponse(b"OK")
    else:
        cursor = connection.cursor()
        query = """select d.id as doctor_id, d.last_name as last_name, d.first_name as first_name, d.patronymic as patronymic,
                    s.id as specialization_id, s.specialization_name as specialization_name
                    from AUTH_USER u join DOCTOR d on (u.id = d.user_id)
                      join DOCTOR_SPECIALIZATION ds on (ds.doctor_id = d.id)
                       join SPECIALIZATION s on (s.id = ds.specialization_id)
                        where (u.id = %s)"""
        cursor.execute(query, [request.user.id])
        current_doctor_info = dictfetchall(cursor)
        request.session["cur_doctor_id"] = current_doctor_info[0]["doctor_id"]
        specializations = [
            {"id": info["specialization_id"], "value": info["specialization_name"]}
            for info in current_doctor_info
        ]
        request.session["last_name"] = current_doctor_info[0]["last_name"]
        request.session["first_name"] = current_doctor_info[0]["first_name"]
        request.session["patronymic"] = current_doctor_info[0]["patronymic"]
        return render(request, "hospitalapp/doctor_index.html", context={
            "last_name":  request.session["last_name"],
            "first_name": request.session["first_name"],
            "patronymic": request.session["patronymic"],
            "specializations": specializations,
        })


class PatientAdmissionView(View):
    def get(self, request):
        if not request.is_ajax():
            specialization_name = request.session["cur_doctor_specialization_name"]
            visit_purposes = VisitPurpose.objects.values()
            admission_types = TypeOfAdmission.objects.values()
            all_dispansery_statuses = DispanseryStatus.objects.values("name")
            if specialization_name == "surgent":
                template_name = "hospitalapp/cardiologist_admission.html"
            elif specialization_name == "cardiologist":
                template_name = "hospitalapp/cardiologist_admission.html"
            elif specialization_name == "therapist":
                template_name = "hospitalapp/therapist_admission.html"
            return render(request, template_name, context={
                "last_name":  request.session["last_name"],
                "first_name": request.session["first_name"],
                "patronymic": request.session["patronymic"],
                "visit_purposes": visit_purposes,
                "admission_types": admission_types,
                "dispansery_statuses": all_dispansery_statuses,
                "action": "review"
            })
        else:
            print(request.GET)
            if request.GET.get("icd10_text"):
                return self._get_icd10_issues(request)
            elif request.GET.get("cur_reviewed_patient_id", None):
                return self._memorize_cur_patient(request)

    def _memorize_cur_patient(self, request):
        cur_patient = int(request.GET["cur_reviewed_patient_id"][0])
        request.session["cur_reviewed_patient_id"] = cur_patient
        return JsonResponse({"status": "OK"}, safe=False)

    def _get_icd10_issues(self, request):
        cursor = connection.cursor()
        pattern = "{}{}{}".format("%", request.GET["icd10_text"], "%")
        query = "select id, code, name from icd10 where (upper(code || name) like upper(%s))"
        cursor.execute(query, [pattern])
        icd10_issues = cursor.fetchall()
        return JsonResponse(icd10_issues, safe=False)

    def post(self, request, *args, **kwargs):
        handled_text_dict = handle_input_text(request.POST)
        cur_doctor_specialization_id = request.session["cur_doctor_specialization_id"]
        cur_patient_id = request.session["cur_reviewed_patient_id"]
        visit_purpose_id = VisitPurpose.objects.get(value=handled_text_dict["visit_purpose"]).id
        admission_type_id = TypeOfAdmission.objects.get(value=handled_text_dict["admission_type"]).id
        admission = PatientsAdmissionToDoctors(
            visit_purpose_id=visit_purpose_id,
            admission_type_id=admission_type_id,
            doctor_specialization_id=cur_doctor_specialization_id,
            patient_id=cur_patient_id,
            admission_datetime=datetime.datetime.now()
        )
        admission.save()
        admission_id = admission.id
        icd10_id = handled_text_dict.get("icd10_id")
        print("dict:", handled_text_dict)
        if icd10_id == "":
            handled_text_dict["icd10_id"] = None


        dispansery_status = handled_text_dict.get("dispansery_status")
        if dispansery_status == "":
            handled_text_dict["dispansery_status"] = None
        else:
            pass
            # dispansery_status_id = DispanseryStatus.objects.get(name=dispansery_status)
            # if dispansery_status == "состоит":
            #
            # elif dispansery_status == "взят":
            #     pass
            # elif dispansery_status == "не показано":
            #     pass
        print(handled_text_dict)
        if visit_purpose_id == 4:
            if handled_text_dict.get("dispanserization_finished") is not None:
                handled_text_dict["dispanserization_finished"] = True
            else:
                handled_text_dict["dispanserization_finished"] = False

                dispansery_status_name = handled_text_dict["dispansery_status"]
                if dispansery_status != "":
                    dispansery_status_id = DispanseryStatus.objects.get(
                        name=dispansery_status_name
                    )["name"]
                    handled_text_dict["dispansery_status"] = dispansery_status_id
        else:
            if handled_text_dict.get("therapy_finished") is not None:
                handled_text_dict["therapy_finished"] = True
            else:
                handled_text_dict["therapy_finished"] = False

        if request.session["cur_specialization_name"] == "cardiologist":
            if visit_purpose_id == 4:
                pass
            else:
                create_cardiologist_review_blank(admission_id, handled_text_dict)
        elif request.session["cur_specialization_name"] == "therapist":
            if visit_purpose_id == 4:
                create_therapist_dispanserization_blank(admission_id, handled_text_dict)
            else:
                create_therapist_review_blank(admission_id, handled_text_dict)
        return render(request, "hospitalapp/cardiologist_admission.html")


def patient_search(request):
    police_type = request.GET.get("police_type", None)
    police_series = request.GET.get("police_series", None)
    police_number = request.GET.get("police_number", None)
    print(police_type, police_series, police_number)
    if police_type == "2":
        police_series = None
    patient_info = Patient.objects.filter(
        medical_police_type=police_type,
        medical_police_series=police_series,
        medical_police_number=police_number
    ).values("id", "last_name", "first_name", "patronymic", "date_birth")
    return JsonResponse(list(patient_info), safe=False)


def find_patients_by_name(request):
    full_name = request.GET["full_name"]
    cursor = connection.cursor()
    pattern = full_name + "%"
    pattern = re.sub(r"[ ]{2,}", " ", pattern)
    query = "select id, last_name, first_name, patronymic, date_birth, medical_police_number" \
            " from patient where (UPPER(last_name||' '||first_name||' '||patronymic) like upper(%s))"
    cursor.execute(query, [pattern])
    return JsonResponse(dictfetchall(cursor), safe=False)


class IssuesHistoryView(View):
    def get(self, request):
        if not request.is_ajax():
            return render(request, "hospitalapp/issues_history.html", context={
                "last_name": request.session["last_name"],
                "first_name": request.session["first_name"],
                "patronymic": request.session["patronymic"],
                "visit_purposes": VisitPurpose.objects.values(),
                "specializations": Specialization.objects.values(),
                "action": "history"
            })
        else:
            print("in issues. params:", request.GET)
            if request.GET.get("full_name"):
                return find_patients_by_name(request)
            elif request.GET.get("patient_id"):
                return self._find_admissions_by_patient(request)
            elif request.GET.get("target") == "get admissions with filter":
                return self._find_patient_admissions_with_filter(request)
            elif request.GET.get("target") == "get admission blank":
                return self._find_review_blank(request)

    def _find_admissions_by_patient(self, request):
        patient_id = request.GET["patient_id"]
        request.session["patient_id"] = patient_id
        cursor = connection.cursor()
        query = """select pa.id as id, vp.value as visit_purpose, d.last_name as doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic,
                         s.specialization_name as doctor_specialization, pa.admission_datetime::DATE as admission_date
                         from patients_admission_to_doctors pa        
                         join doctor_specialization ds on (ds.id = pa.doctor_specialization_id)
                         join doctor d on (d.id = ds.doctor_id)
                         join specialization s on (s.id = ds.specialization_id)
                         join visit_purpose vp on (pa.visit_purpose_id = vp.id)
                          WHERE (patient_id = %s)
                           ORDER by pa.admission_datetime DESC ;"""
        cursor.execute(query, [patient_id])
        res = dictfetchall(cursor)
        cache.set("all_patient_admissions", res)
        return JsonResponse(res, safe=False)

    def _find_patient_admissions_with_filter(self, request):
        date_from = request.GET.get("date_from", None)
        date_to = request.GET.get("date_to", None)
        visit_purpose = request.GET.get("visit_purpose", None)
        specialization = request.GET.get("specialization", None)
        all_admissions = cache.get("all_patient_admissions")
        if all_admissions is None:
            patient_id = request.session["patient_id"]
            cursor = connection.cursor()
            query = """select s.id as specialization_id, pa.id as id, vp.value as visit_purpose, d.last_name as doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic,
                                     s.specialization_name as doctor_specialization, pa.admission_datetime::DATE as admission_date
                                     from patients_admission_to_doctors pa        
                                     join doctor_specialization ds on (ds.id = pa.doctor_specialization_id)
                                     join doctor d on (d.id = ds.doctor_id)
                                     join specialization s on (s.id = ds.specialization_id)
                                     join visit_purpose vp on (pa.visit_purpose_id = vp.id)
                                      WHERE (patient_id = %s) ORDER by pa.admission_datetime DESC;"""
            cursor.execute(query, [patient_id])
            all_admissions = dictfetchall(cursor)
            cache.set("all_patient_admissions", all_admissions)
        admissions_with_filter = [
            admission for admission in all_admissions
            if datetime.datetime.strptime(date_from, "%d.%m.%Y").date()
               <= admission["admission_date"] <=
               datetime.datetime.strptime(date_to, "%d.%m.%Y").date()
               and (admission["visit_purpose"] == visit_purpose or not visit_purpose)
               and (admission["doctor_specialization"] == specialization or not specialization)
        ]
        return JsonResponse(admissions_with_filter, safe=False)

    def _find_review_blank(self, request):
        admission_id = request.GET.get("admission_id")
        specialization_id = PatientsAdmissionToDoctors.objects.filter(id=admission_id).values_list(
            "doctor_specialization__specialization_id"
        )[0][0]
        print("specialuzation_id:", specialization_id)
        if specialization_id == 1:  #surgent
            pass
        elif specialization_id == 2:  #cardiologist
            admission_blank = CardiologistAdmissionReview.objects.filter(
                admission_id=admission_id
            ).values()[0]
            try:
                icd10_name = Icd10.objects.get(id=admission_blank["icd10_id"])
            except ObjectDoesNotExist:
                icd10_name = ""
            admission_blank["icd10_name"] = icd10_name
            admission_blank["last_name"] = request.session["last_name"]
            admission_blank["first_name"] = request.session["first_name"]
            admission_blank["patronymic"] = request.session["patronymic"]
            print(admission_blank["last_name"])
            return render(request, "hospitalapp/cardiologist_admission_blank.html", context=admission_blank)


class DispanserizationStatusView(View):
    def get(self, request):
        query = "select p.last_name, p.first_name, p.patronymic, p.date_birth, p.medical_police_number " \
                " from "


class AppointmentFromDoctorView(View):
    def get(self, request):
        if not request.is_ajax():
            specializations = Specialization.objects.values()
            last_name = request.session["last_name"]
            first_name = request.session["first_name"]
            patronymic = request.session["patronymic"]
            return render(
                request, "hospitalapp/appointment_from_doctor.html",
                          context={
                              "specializations": specializations,
                              "last_name": last_name,
                              "first_name": first_name,
                              "patronymic": patronymic,
                              "action": "appointment"
                          }
            )
        else:
            if request.GET.get("full_name"):
                return find_patients_by_name(request)
            elif request.GET.get("patient_id"):
                request.session["patient_id"] = request.GET["patient_id"]
                return JsonResponse({"status": "OK"})
            elif request.GET.get("specialization_id") and request.GET.get("appointment_date"):
                request.session["specialization_id"] = request.GET["specialization_id"]
                request.session["appointment_date"] = request.GET["appointment_date"]
                return self._get_available_doctors_on_date(request)
            elif request.GET.get("doctor_id"):
                request.session["doctor_id"] = request.GET["doctor_id"]
                return self._get_time_on_date_and_doctor(request)
            else:
                raise Exception("No any params in ajax request for appointement from doctor")

    def post(self, request):
        if request.is_ajax():
            appointment_id = request.POST.get("appointment_id")
            patient_id = request.session.get("patient_id")
            print("patient id:", patient_id)
            doctor_id = request.session.get("doctor_id")
            cur_doctor_id = request.session.get("cur_doctor_id")
            if appointment_id and patient_id:
                rows_num = PatientsAppointmentToDoctors.objects.filter(
                    id=appointment_id, free=True
                ).update(
                    patient_id=patient_id,
                    free=False,
                    doctor_sender_id=cur_doctor_id
                )
                if rows_num:
                    return JsonResponse({"status": "OK"})
                else:
                    return JsonResponse({"status": "FAIL"})
            else:
                raise Exception(
                    "Not enough information for patient appointment: "
                    "appointment_id:{}, patient_id:{}, doctor_id:{}".
                        format(appointment_id, patient_id, doctor_id)
                )

    def _get_available_doctors_on_date(self, request):
        specialization_id = request.session["specialization_id"]
        appointment_date = request.session["appointment_date"]
        appointment_date = datetime.datetime.strptime(appointment_date, "%d/%m/%Y").date()
        query = "select d.id as doctor_id, d.last_name doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic from patients_appointment_to_doctors pa" \
                " join doctor_specialization ds on (ds. id = pa.doctor_specialization_id)" \
                " join doctor d on (d.id = ds.doctor_id) where (ds.specialization_id = %s and pa.appointment_datetime::date =%s);"
        cursor = connection.cursor()
        cursor.execute(query, [specialization_id, appointment_date])
        doctors_on_date = dictfetchall(cursor)
        return JsonResponse(doctors_on_date, safe=False)

    def _get_time_on_date_and_doctor(self, request):
        doctor_id = request.session["doctor_id"]
        appointment_date = request.session["appointment_date"]
        specialization_id = request.session["specialization_id"]
        cursor = connection.cursor()
        query = "select pa.id as id, to_char(pa.appointment_datetime, 'HH:MI') as time, pa.free as free from patients_appointment_to_doctors pa " \
                " join doctor_specialization ds on (ds.id = pa.doctor_specialization_id)" \
                " where (ds.doctor_id = %s and pa.appointment_datetime::DATE = %s and ds.specialization_id = %s and pa.appointment_datetime > %s)"
        cursor.execute(query, [doctor_id, appointment_date, specialization_id, datetime.datetime.now()+datetime.timedelta(minutes=1)])
        return JsonResponse(dictfetchall(cursor), safe=False)


def review_blank(request, admission_id):
    cursor = connection.cursor()
    query = "select s.specialization_name as specialization_name from patients_admission_to_doctors pa" \
            " JOIN doctor_specialization ds on (pa.doctor_specialization_id = ds.id)" \
            " JOIN specialization s on (s.id = ds.specialization_id)" \
            " where (pa.id = %s)"
    cursor.execute(query, [admission_id])
    specialization_name = cursor.fetchone()[0]
    admission = PatientsAdmissionToDoctors.objects.get(id=admission_id)

    if specialization_name == "therapist":
        if admission.visit_purpose_id == 4:
            blank = TherapistAdmissionDispanserization.objects.filter(
                admission_id=admission_id
            ).values()[0]
            print("therapist dispanserization")
            template_name = "hospitalapp/therapist_dispanserization_blank.html"
        else:
            blank = TherapistAdmissionReview.objects.filter(
                admission_id=admission_id
            ).values()[0]
            print("therapist active")
            template_name = "hospitalapp/therapist_review_blank.html"
    elif specialization_name == "cardiologist":
        if admission.visit_purpose_id == 4:
            pass
        else:
            blank = CardiologistAdmissionReview.objects.filter(
                admission_id=admission_id
            ).values()[0]
            template_name = "hospitalapp/cardiologist_review_blank.html"

    icd10_id = blank["icd10_id"]
    if icd10_id is None:
        blank["icd10_value"] = "Не указано"
    else:
        icd10_code, icd10_name = Icd10.objects.filter(id=icd10_id).values("code", "name")[0]
        blank["icd10_value"] = " ".join([icd10_code, icd10_name])

    return render(request, template_name, context=blank)

