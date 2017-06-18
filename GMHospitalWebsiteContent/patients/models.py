from __future__ import unicode_literals

from django.db import models

class Data(models.Model):

    patientID = models.AutoField(primary_key=True)
    aadharNumber = models.CharField(max_length=12)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=6)
    Age = models.IntegerField()
    Address = models.CharField(max_length=700)
    mobile = models.CharField(max_length=13)
    dateOfRegister = models.DateTimeField()

class Appointments(models.Model):

    patientID = models.IntegerField()
    appointmentNumber = models.AutoField(primary_key=True)
    dateOfAppointment = models.DateTimeField()
    Problems = models.CharField(max_length=1000)

class AdminLogin(models.Model):

    loginAlias = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=100, primary_key=True)


class Logins(models.Model):

    loginAlias = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    approved = models.CharField(max_length=1)
    email = models.CharField(max_length=100, primary_key=True)