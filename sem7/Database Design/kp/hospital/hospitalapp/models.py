# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


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


class Dispanserization(models.Model):
    dispanserization_id = models.AutoField(primary_key=True)
    dispanserization_group = models.CharField(max_length=5)
    icd10_code = models.ForeignKey('Icd10', models.DO_NOTHING, db_column='icd10_code', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dispanserization'


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


class DoctorSpecialization(models.Model):
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField(max_length=100)


    class Meta:
        managed = False
        db_table = 'doctor_specialization'


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, blank=True, null=True)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1)
    passport = models.CharField(max_length=20)
    dispanserization_activity = models.IntegerField()
    joining_staff = models.BooleanField()
    specialization = models.ForeignKey(DoctorSpecialization, models.DO_NOTHING, blank=True, null=True)
    telephone_num = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee'


class Icd10(models.Model):
    icd10_code = models.CharField(primary_key=True, max_length=20)
    subclass = models.ForeignKey('Icd10Subclass', models.DO_NOTHING, db_column='subclass')
    class_field = models.ForeignKey('Icd10Class', models.DO_NOTHING, db_column='class')  # Field renamed because it was a Python reserved word.

    class Meta:
        managed = False
        db_table = 'icd10'


class Icd10Class(models.Model):
    class_field = models.CharField(db_column='class', primary_key=True, max_length=20)  # Field renamed because it was a Python reserved word.
    class_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'icd10_class'


class Icd10Subclass(models.Model):
    subclass = models.CharField(primary_key=True, max_length=20)
    subclass_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'icd10_subclass'


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    patronymic = models.CharField(max_length=40, blank=True, null=True)
    date_birth = models.DateField()
    sex = models.CharField(max_length=1)
    medical_policynum = models.CharField(max_length=30)
    check_out_date = models.DateField(blank=True, null=True)
    passport = models.CharField(max_length=20)
    tel_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'


class PatientsAdmission(models.Model):
    dispanserization = models.ForeignKey(Dispanserization, models.DO_NOTHING, blank=True, null=True)
    admission_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    admission_time = models.DateTimeField()
    icd10_code = models.ForeignKey(Icd10, models.DO_NOTHING, db_column='icd10_code', blank=True, null=True)
    symtoms = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_admission'


class PatientsAppointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    appointment_time = models.DateTimeField()
    free = models.BooleanField()
    patient = models.ForeignKey(Patient, models.DO_NOTHING)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patients_appointment'


class RegistrationOfSickPeople(models.Model):
    registration_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, models.DO_NOTHING)
    specialization = models.ForeignKey(DoctorSpecialization, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'registration_of_sick_people'
