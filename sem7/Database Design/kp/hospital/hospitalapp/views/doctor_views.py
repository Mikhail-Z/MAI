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
from django.template import Template, Context
from django.forms.models import model_to_dict


class DoctorLoginView(View):

    def get(self, request, *args, **kwargs):
        request.session["redirect_url"] = request.GET.get("next")
        return render(request, "hospitalapp/doctor_login.html")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.session.get("redirect_url") is not None:
                redirect_url = request.session.pop("redirect_url")
            else:
                redirect_url = "/doctor/"
            return HttpResponseRedirect(redirect_url)
        else:
            return render(request, "hospitalapp/doctor_login.html", context={"after_wrong_login": True})


def index(request):
    if request.method == 'GET':
        afterRequest = request.GET.get('afterAction', None)
        print("after request", afterRequest, request.is_ajax())
        if afterRequest:
            return JsonResponse({'redirect': reverse('hospitalapp:index')})
        else:
            return render(request, 'hospitalapp/index.html')


@login_required(login_url="/doctor/login/")
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
            specialization_id = request.session["cur_specialization_id"]
            visit_purposes = VisitPurpose.objects.values()
            admission_types = TypeOfAdmission.objects.values()
            all_dispansery_statuses = DispanseryStatus.objects.values("name")
            if specialization_id == "2":  # кардиолог
                template_name = "hospitalapp/review_blank/cardiologist/cardiologist_admission.html"
            elif specialization_id == "4": # терапевт
                template_name = "hospitalapp/review_blank/therapist/therapist_admission.html"
            else:
                template_name = "hospitalapp/review_blank/general_prevention_specialist/admission.html"

            specializations = Specialization.objects.filter(is_hidden=False).values("specialization_name")


            return render(request, template_name, context={
                "last_name":  request.session["last_name"],
                "first_name": request.session["first_name"],
                "patronymic": request.session["patronymic"],
                "visit_purposes": visit_purposes,
                "admission_types": admission_types,
                "dispansery_statuses": all_dispansery_statuses,
                "action": "review",
                "specializations": list(specializations),
            })
        else:
            if request.GET.get("icd10_text"):
                return self._get_icd10_issues(request)
            elif request.GET.get("cur_reviewed_patient_id"):
                cur_patient = int(request.GET["cur_reviewed_patient_id"])
                request.session["cur_reviewed_patient_id"] = cur_patient
                return self._get_procedures_and_specializations(request)

    def _get_procedures_and_specializations(self, request):
        cur_patient_id = request.session["cur_reviewed_patient_id"]
        patient_info = Patient.objects.get(id=int(cur_patient_id))
        patient_age = datetime.datetime.now().year - patient_info.date_birth.year
        patient_sex = patient_info.sex
        second_stage_procedures = Research.objects.filter(Q(age_begin__lte=patient_age),
                                                          Q(age_end__gt=patient_age),
                                                          Q(sex=patient_sex)|Q(sex="fm")).values("name")
        second_stage_specializations = SpecializationsForDispanserization.objects.filter(stage=2).values("specialization__specialization_name")

        first_stage_procedures = Research.objects.filter(stage=1).values("name")
        first_stage_specializations = SpecializationsForDispanserization.objects.filter(stage=1).values("specialization__specialization_name")

        print(list(second_stage_specializations))
        return JsonResponse({
            "second_stage_specializations": list(second_stage_specializations),
            "second_stage_procedures": list(second_stage_procedures),
            "first_stage_procedures": list(first_stage_procedures),
            "first_stage_specializations": list(first_stage_specializations)
        }, safe=False)

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

        try:
            admission_type_id = TypeOfAdmission.objects.get(value=handled_text_dict["admission_type"]).id
        except ObjectDoesNotExist:
            admission_type_id = None

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
        if icd10_id == "":
            handled_text_dict["icd10_id"] = None


        dispansery_status = handled_text_dict.get("dispansery_status", "")
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

        if visit_purpose_id == 4:
            if handled_text_dict.get("dispanserization_finished") is not None:
                handled_text_dict["dispanserization_finished"] = True
            else:
                handled_text_dict["dispanserization_finished"] = False

                dispansery_status_name = handled_text_dict["dispansery_status"]
                if dispansery_status != "":
                    dispansery_status_id = DispanseryStatus.objects.get(
                        name=dispansery_status_name
                    ).name
                    handled_text_dict["dispansery_status"] = dispansery_status_id

            dispansery_status_name = handled_text_dict["dispansery_status"]
            if dispansery_status_name is not None:
                handled_text_dict["dispansery_status"] = DispanseryStatus.objects.filter(name=dispansery_status_name).get()
                handled_text_dict["dispansery_status_id"] = handled_text_dict["dispansery_status"].id
            else:
                handled_text_dict["dispansery_status_id"] = None

            if handled_text_dict.get("dispanserization_stage") == "":
                handled_text_dict["dispanserization_stage"] = None

            cursor = connection.cursor()
            cursor.execute("begin")

            cursor.callproc(
                "update_dispanserization_status",
                (
                    cur_patient_id,
                    handled_text_dict["dispansery_status_id"],
                    handled_text_dict.get("health_group", None),
                    handled_text_dict.get("dispanserization_finished", None),
                    handled_text_dict.get("dispanserization_stage", None),
                    admission.admission_datetime
                )
            )
        else:
            if handled_text_dict.get("therapy_finished") is not None:
                handled_text_dict["therapy_finished"] = True
            else:
                handled_text_dict["therapy_finished"] = False

        if request.session["cur_specialization_id"] == "2":  # кардиолог
            create_cardiologist_review_blank(admission_id, handled_text_dict)
        elif request.session["cur_specialization_id"] == "4":  # терапевт
            if visit_purpose_id == 4:
                create_therapist_dispanserization_blank(admission_id, handled_text_dict)
            else:
                create_therapist_review_blank(admission_id, handled_text_dict)
        else:
            create_general_prevention_dispanserization_blank(admission_id, handled_text_dict)

        return JsonResponse({"id": admission_id}, safe=False)


def patient_search(request):
    police_type = request.GET.get("police_type")
    police_series = request.GET.get("police_series")
    police_number = request.GET.get("police_number")
    ticket_number = request.GET.get("ticket_number")
    if ticket_number:
        try:
            patient_id = PatientsAppointmentToDoctors.objects.filter(ticket=ticket_number).order_by("appointment_datetime")[0]
            patient_info = Patient.objects.filter(id=patient_id).values("id", "last_name", "first_name", "patronymic", "date_birth")
        except IndexError:
            patient_info = Patient.objects.none()
    else:
        if police_type == "2":
            police_series = None
        patient_info = Patient.objects.filter(
            medical_police_type=police_type,
            medical_police_series=police_series,
            medical_police_number=police_number
        ).values("id", "last_name", "first_name", "patronymic", "date_birth")
    print("patient_into:", patient_info)
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
        request.session["patient_i  d"] = patient_id
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
        if request.is_ajax():
            return self._get_dispanserizations_by_filter(request)

        query = """SELECT count(id) as patients_for_dispanserization_count from patient p
                    where (extract(year from now()) - extract(YEAR FROM p.date_birth)) >= 21 
                    and (extract(year from now()) - extract(YEAR FROM p.date_birth))::int % 3 = 0"""
        cursor = connection.cursor()
        cursor.execute(query)

        insurance_medical_organizations = InsuranceMedicalOrganization.objects.values()
        dispansery_statuses = DispanseryStatus.objects.values()


        patients_for_dispanserization_count = dictfetchall(cursor)[0]["patients_for_dispanserization_count"]

        cursor = connection.cursor()
        cursor.execute("select DISTINCT EXTRACT(YEAR from last_visit_datetime)::INT as year FROM dispanserization_status;")
        dispanserization_years = dictfetchall(cursor)

        return render(request, "hospitalapp/dispanserization_status.html", context={
            "patients_for_dispanserization_count": patients_for_dispanserization_count,
            "insurance_medical_organizations": insurance_medical_organizations,
            "dispansery_statuses": dispansery_statuses,
            "last_name": request.session["last_name"],
            "first_name": request.session["first_name"],
            "patronymic": request.session["patronymic"],
            "dispanserization_years": dispanserization_years,
            "action": "dispanserization"
        })

    def _get_dispanserizations_by_filter(self, request):
        age_from = request.GET.get("age_from") if request.GET.get("age_from") != "" else 21
        age_to = request.GET.get("age_to") if request.GET.get("age_to") != \
                                              "" else 1000
        # query = """
        #     select p.date_birth as patient_date_birth, p.id as patient_id, p.last_name as patient_last_name, p.first_name as patient_first_name, p.patronymic as patient_patronymic, ds.cur_stage as cur_stage, ds.finished as finished, ds.icd10_ids
        #     from patient p left JOIN dispanserization_status ds on (ds.patient_id = p.id)
        #     where ((extract(year from now()) - extract(YEAR FROM p.date_birth)) >= 21
        #             and ((extract(year from now()) - extract(YEAR FROM p.date_birth))::int % 3 = 0)
        #             and (ds.health_group = '{health_group}' or '{health_group}' = '')
        #             and (p.insurance_medical_organization_id::VARCHAR = '{insurance_medical_organization}' or '{insurance_medical_organization}' = '')
        #             and (ds.dispansery_status_id::VARCHAR = '{dispansery_status_id}' or '{dispansery_status_id}' = '')
        #             and ('{dispanserization_year}' = '' or EXTRACT(year from ds.last_visit_datetime)::VARCHAR = '{dispanserization_year}')
        #             ) filtered_dispanserization_status
        #             cross JOIN
        #             (WITH RECURSIVE BFS AS (
        #                 SELECT
        #                   icd10.id        AS vertex_id,
        #                   icd10.parent_id AS parent_id,
        #                   icd10.code      AS code,
        #                   icd10.name      AS name
        #                 FROM icd10
        #                 WHERE icd10.id = '{icd10_id}'
        #count(id) as patients_for_dispanserization_count
        #                 UNION ALL
        #
        #                 SELECT
        #                   icd10.id,
        #                   icd10.parent_id,
        #                   icd10.code,
        #                   icd10.name
        #                 FROM icd10
        #                   JOIN BFS ON icd10.parent_id = BFS.vertex_id
        #               ) SELECT vertex_id from BFS) tmp
        #               where (tmp.vertex_id = ANY(filtered_dispanserization_status.icd10_ids))
        # """.format(
        #     insurance_medical_organization=request.GET.get("insurance_medical_organization", ''),
        #     health_group=request.GET.get("health_group", ''),
        #     dispansery_status_id=request.GET.get("dispansery_status", ""),
        #     dispanserization_year=request.GET.get("dispanserization_year", ""),
        #     icd10_id=request.GET.get("icd10_id", "")
        # )
        query = """SELECT p.last_name as patient_last_name, p.first_name as patient_first_name, p.patronymic as patient_patronymic, p.date_birth as patient_datebirth, p.id as patient_id from patient p
                            where ((extract(year from now()) - extract(YEAR FROM p.date_birth)) >= 21 
                            and (extract(year from now()) - extract(YEAR FROM p.date_birth))::int % 3 = 0
                            and (p.sex = '{sex}' or '{sex}' = 'Не выбрано')
                            and ((extract(year from now()) - extract(YEAR FROM p.date_birth)) >= {age_from})
                            and ((extract(year from now()) - extract(YEAR FROM p.date_birth)) <= {age_to}))""".\
            format(sex=request.GET.get("sex", "Не выбрано"), age_from=age_from, age_to=age_to)
        cursor = connection.cursor()
        cursor.execute(query)
        filtered_patients_for_dispanserization = dictfetchall(cursor)
        """if request.GET.get("current_dispanserization_stage") == "-1":  # Диспансеризация не начата
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if patient["cur_stage"] is not None:
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]

        elif request.GET.get("current_dispanserization_stage") == "0":  # Диспансеризация начата
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if patient["cur_stage"] is None:
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]

        elif request.GET.get("current_dispanserization_stage") == "01":  # В процессе 1-го этапа
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if patient["cur_stage"] != 0:
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]

        elif request.GET.get("current_dispanserization_stage") == "1":  # Диспансеризация окончена на 1-ом этапе
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if not(patient["cur_stage"] == 1 and patient["finished"] is True):
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]

        elif request.GET.get("current_dispanserization_stage") == "12": # В процессе 2-го этапа
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if not ((patient["cur_stage"] == 1 or patient["cur_stage"] == 2) and patient["finished"] == False):
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]
        elif request.GET.get("current_dispanserization_stage") == "2": # Закончена на 2-ом этапе
            for i, patient in enumerate(filtered_patients_for_dispanserization.copy()):
                if not (patient["cur_stage"] == 2 or patient["finished"] is True):
                    filtered_patients_for_dispanserization = filtered_patients_for_dispanserization[:i] \
                                                             + filtered_patients_for_dispanserization[i+1:]"""
        return JsonResponse(filtered_patients_for_dispanserization, safe=False)


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
        query = "select d.id as doctor_id, d.last_name as doctor_last_name, d.first_name as doctor_first_name, d.patronymic as doctor_patronymic from patients_appointment_to_doctors pa" \
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
        query = "select pa.id as id, to_char(pa.appointment_datetime, 'HH24:MI') as time, pa.free as free from patients_appointment_to_doctors pa " \
                " join doctor_specialization ds on (ds.id = pa.doctor_specialization_id)" \
                " where (ds.doctor_id = %s and pa.appointment_datetime::DATE = %s and ds.specialization_id = %s and pa.appointment_datetime > %s)"
        cursor.execute(query, [doctor_id, appointment_date, specialization_id, datetime.datetime.now()+datetime.timedelta(minutes=1)])
        return JsonResponse(dictfetchall(cursor), safe=False)


def review_blank(request, admission_id):
    for_print = request.GET.get("print")
    cursor = connection.cursor()
    query = "select ds.specialization_id as specialization_id from patients_admission_to_doctors pa" \
            " JOIN doctor_specialization ds on (pa.doctor_specialization_id = ds.id)" \
            " where (pa.id = %s)"
    cursor.execute(query, [admission_id])
    specialization_id = cursor.fetchone()[0]
    admission = PatientsAdmissionToDoctors.objects.get(id=admission_id)
    if specialization_id == 4:  # терапевт
        if admission.visit_purpose_id == 4:
            blank = TherapistAdmissionDispanserization.objects.filter(
                admission_id=admission_id
            ).values()[0]
            if for_print == "true":
                template_name = "hospitalapp/review_blank/therapist/therapist_dispanserization_blank_print.html"
            else:
                template_name = "hospitalapp/review_blank/therapist/therapist_dispanserization_blank.html"
            try:
                blank["dispansery_status"] = DispanseryStatus.objects.get(id=blank["dispansery_status_id"]).name
            except ObjectDoesNotExist:
                blank["dispansery_status"] = "Не указано"
        else:
            blank = TherapistAdmissionReview.objects.filter(
                admission_id=admission_id
            ).values()[0]
            if for_print == "true":
                template_name = "hospitalapp/review_blank/therapist/therapist_review_blank_print.html"
            else:
                template_name = "hospitalapp/review_blank/therapist/therapist_review_blank.html"

    elif specialization_id == 2:  # кардиолог
        if admission.visit_purpose_id == 4:
            blank = CardiologistAdmissionDispanserization.objects.filter(
                admission_id=admission_id
            ).values()[0]
            if for_print == "true":
                template_name = "hospitalapp/review_blank/cardiologist/cardiologist_dispanserization_blank_print.html"
            else:
                template_name = "hospitalapp/review_blank/cardiologist/cardiologist_dispanserization_blank.html"
            try:
                blank["dispansery_status"] = DispanseryStatus.objects.get(id=blank["dispansery_status_id"]).name
            except ObjectDoesNotExist:
                blank["dispansery_status"] = "Не указано"
        else:
            blank = CardiologistAdmissionReview.objects.filter(
                admission_id=admission_id
            ).values()[0]
            if for_print == "true":
                template_name = "hospitalapp/review_blank/cardiologist/cardiologist_review_blank_print.html"
            else:
                template_name = "hospitalapp/review_blank/cardiologist/cardiologist_review_blank.html"
    else:
        if admission.visit_purpose_id == 4:
            blank = GeneralPreventionDispanserizationBlank.objects.filter(
                admission_id=admission_id
            ).values()[0]
            if for_print == "true":
                template_name = "hospitalapp/review_blank/general_prevention_specialist/general_prevention_blank_print.html"
            else:
                template_name = "hospitalapp/review_blank/general_prevention_specialist/general_prevention_blank.html"

    icd10_id = blank.get("icd10_id")
    if icd10_id is None:
        blank["icd10_value"] = "Не указано"
    else:
        icd10_name = Icd10.objects.get(id=icd10_id).name
        blank["icd10_value"] = icd10_name

    for key in blank.keys():
        if blank[key] is None or blank[key] == "":
            blank[key] = "Не указано"

    last_name = request.session["last_name"]
    first_name = request.session["first_name"]
    patronymic = request.session["patronymic"]
    blank["last_name"] = last_name
    blank["first_name"] = first_name
    blank["patronymic"] = patronymic
    patient = Patient.objects.get(id=admission.patient_id)
    blank["patient"] = model_to_dict(patient)
    blank["admission_datetime"] = admission.admission_datetime
    return render(request, template_name, context=blank)

