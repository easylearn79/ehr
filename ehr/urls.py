from django.urls import path
from . import views

from .views import PatientDetailView,AddPatientView,AddPharmacyView, PharmacyList,LabView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('stafflogin/', views.stafflogin, name='stafflogin'),
    path('staffsignup/', views.staffsignup, name='staffsignup'),
    path('staffsignup_view/', views.staffsignup_view, name='staffsignup_view'),
    path('stafflogin_view/', views.stafflogin_view, name='stafflogin_view'),
    path('patientlogin/', views.patientlogin, name='patientlogin'),
    path('patientlogin_view/', views.patientlogin_view, name='patientlogin_view'),
    #path(r'patientsignup/$', views.patientsignup, name='patientsignup'),
    path('patientsignup/', AddPatientView.as_view(), name='patientsignup'),
    path('add_drug/', AddPharmacyView.as_view(), name='add_drug'),
    path('lab/', views.lab, name='lab'),
    path('list/', views.pharmacylist, name='list'),
    path('patientsignup_view/', views.patientsignup_view, name='patientsignup_view'),
    path('getselectedpatient/', views.getSelectedPatient, name = 'getSelectedPatient'),
    path('getselectedpatient/LabResults.txt/', views.LabResults),
    path('getselectedpatient/Diagnoses.txt/', views.Diagnoses),
    path('getselectedpatient/Medication.txt/', views.Medication),
    path('getselectedpatient/Prescription.txt/', views.Prescription),
    path('getselectedpatient/DoctorNotes.txt/', views.DoctorNotes),
    path('getselectedpatient/Allergies.txt/', views.Allergies),
    path('getselectedpatient/BillingInfo.txt/', views.BillingInfo),
    path('searchEHR/', views.search, name = 'search'),
    path('consult/', views.consult, name='consult'),
    path('patientfile/', views.manage_patient, name='manage_patient'),
    path('drugview/', views.drugview, name='drug'),
    path('<slug:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('pharmacy/', views.pharmacydetail, name='pharmacy'),
    path('patient_search/', views.patient_search, name='patient_search'),

    
]