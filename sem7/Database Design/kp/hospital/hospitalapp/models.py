# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AdmissionResult(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admission_result'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cabinet(models.Model):
    number = models.CharField(max_length=5)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cabinet'


class Dispanserization(models.Model):
    dispanserization_group = models.CharField(max_length=5)
    icd10 = models.ForeignKey('Icd10', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispanserization'


class DispensaryRegistration(models.Model):
    patient_id = models.IntegerField()
    specialization = models.ForeignKey('Specialization', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispensary_registration'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctor(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, blank=True, null=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1)
    passport = models.CharField(max_length=20)
    dispanserization_activity = models.IntegerField()
    joining_staff = models.BooleanField()
    tel_number = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    specialization = models.ForeignKey('Specialization', models.DO_NOTHING, blank=True, null=True)
    qualification = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor'


class DoctorSpecialization(models.Model):
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, blank=True, null=True)
    specialization = models.ForeignKey('Specialization', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctor_specialization'


class Icd10(models.Model):
    code = models.TextField()
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'icd10'


class Patient(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, blank=True, null=True)
    date_birth = models.DateField()
    sex = models.CharField(max_length=1)
    check_out_date = models.DateField(blank=True, null=True)
    passport = models.CharField(max_length=20, blank=True, null=True)
    tel_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    snils = models.CharField(max_length=20, blank=True, null=True)
    medical_police_type = models.SmallIntegerField(blank=True, null=True)
    medical_police_series = models.CharField(max_length=8, blank=True, null=True)
    medical_police_number = models.CharField(max_length=20, blank=True, null=True)
    dispanserization_agreement = models.NullBooleanField()
    blood_group = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'patient'


class PatientsAdmissionToDoctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    admission_datetime = models.DateTimeField()
    symtoms = models.TextField(blank=True, null=True)
    icd10 = models.ForeignKey(Icd10, models.DO_NOTHING, blank=True, null=True)
    admission_type = models.ForeignKey('TypeOfAdmission', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_admission_to_doctors'


class PatientsAdmissionToProcedures(models.Model):
    id = models.BigAutoField(primary_key=True)
    admission_datetime = models.DateTimeField(blank=True, null=True)
    free = models.NullBooleanField()
    doctor_sender = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctor_sender', blank=True, null=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_admission_to_procedures'


class PatientsAppointmentToDoctors(models.Model):
    id = models.BigAutoField(primary_key=True)
    appointment_datetime = models.DateTimeField()
    free = models.BooleanField()
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    visit_purpose = models.ForeignKey('VisitPurpose', models.DO_NOTHING)
    doctor_sender = models.ForeignKey(Doctor, models.DO_NOTHING)
    payment_type = models.ForeignKey('PaymentType', models.DO_NOTHING, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, models.DO_NOTHING)
    doctor_specialization = models.ForeignKey(DoctorSpecialization, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_appointment_to_doctors'


class PaymentType(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'payment_type'


class Specialization(models.Model):
    specialization_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'specialization'


class TypeOfAdmission(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'type_of_admission'


class VisitPurpose(models.Model):
    id = models.IntegerField(primary_key=True)
    value = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'visit_purpose'
