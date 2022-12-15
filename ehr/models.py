from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
# Create your models here. 


class PatientInfo(models.Model):
    USER_TYPE = ((1, "HOD"), (2, "Staff"))
    GENDER = [("M", "Male"), ("F", "Female")]
    BLOOD_GROUP = [("A", "A+"), ("A", "A-"),("B+", "B+"), ("B-", "B-"),("O+", "O+"), ("O-", "O-"),("AB+", "AB+"), ("AB-", "AB-")]
    GENOTYPE = [("AA", "AA"), ("AS", "AS"),("AC", "AC"), ("SS", "SS"), ("G", "SC")]
    MARITAL_STATUS = [("SINGLE", "SINGLE"), ("WIDOWED", "WIDOWED"), ("DIVORCED", "DIVORCED"), ("SEPARATED", "SEPARATED")]
    id = models.AutoField(primary_key=True)
    patientName = models.CharField(max_length=25, unique=True)
    patientPassword = models.TextField(max_length=25)
    secret_key = models.CharField(max_length=25)
    purpose = models.CharField(max_length=500)
    doctorName = models.CharField(max_length=254)
    patientHward = models.CharField(max_length=25)
    Date_of_Birth = models.DateField()
    Gender = models.CharField(max_length = 150,  choices=GENDER)
    Marital_status = models.CharField(max_length=50,  choices= MARITAL_STATUS)
    Blood_Group = models.CharField(max_length=100, choices=BLOOD_GROUP)
    Genotype = models.CharField(max_length=30,choices=GENOTYPE)
    Phone_no = models.IntegerField()
    Illness = models.CharField(max_length=250)
    Medical_history = models.TextField()
    Resident_Address = models.CharField(max_length=300)
    Allegies = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs = {"pk": str(self.pk)})


        


class Consultant(models.Model):
    patient_id = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    Lab_test = models.CharField(max_length=300)
    Doctor_diagnostic = models.CharField(max_length=300)
    Doctor_Observation = models.CharField(max_length=300)
    Medication = models.CharField(max_length=300)
    Recommendation = models.CharField(max_length=300)
    Doctor = models.CharField(max_length=300)
    visit_time = models.CharField(max_length=300)
    result = models.CharField(max_length=300)


class Pharmacy(models.Model):
    Drug_name = models.CharField(max_length=300)
    Cost = models.CharField(max_length=300)
    Category = models.CharField(max_length=300)
    Selling_price = models.CharField(max_length=300)
    Qty = models.CharField(max_length=300)
    Man_date = models.DateField()
    Exp_date = models.DateField(auto_now=False, auto_now_add=False)


class Laboratory(models.Model):
    patient_id = models.ForeignKey(PatientInfo, on_delete=models.CASCADE)
    result = models.CharField(max_length=300)
    sample_type = models.CharField(max_length=300)



class StaffInfo(models.Model):
	id = models.AutoField(primary_key=True)
	uid = models.TextField(max_length=25)
	username = models.TextField(max_length=254)
	password = models.TextField(max_length=25)
	role = models.TextField(max_length=50)
	certification = models.TextField(max_length=25)
	specialization = models.TextField(max_length=50)
	hward = models.TextField(max_length=25)




