from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import  PatientInfo, StaffInfo,Laboratory,Consultant, Pharmacy
from django.http import HttpResponse
import time
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from rdflib import Graph, URIRef
from django.urls import reverse
import os
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .form import PatientForm, PharmacyForm
from django_unicorn.components import UnicornView



searchtoken = []
loggedinUsers = []
attributes = []
Allowed_Fields = []



# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("admin_home"))
        elif request.user.user_type == '2':
            return redirect(reverse("staff_home"))
    return render(request, 'authfr/log.html')


def doLogin(request, **kwargs):
    # Authenticate
    user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
    if user != None:
        login(request, user)
        if user.user_type == '1':
            return redirect(reverse(" "))
        elif user.user_type == '2':
            return redirect(reverse("staff_home"))
    else:
        messages.error(request, "Invalid details")
        return redirect("home")


class SearchView(UnicornView):
    patient = ""
    all_patient = PatientInfo.objects.all()

    def Clear_Patient(self):
        self.patient = ""


    def patients(self):
        if not self.patient:
            return []
        
        return [p for p in self.all_patient]

    class Meta:
        exclude = ('all_patient')



class PatientDetailView(DetailView):
    model = PatientInfo
    template_name = "profile.html"



def manage_patient(request):
    patient = PatientInfo.objects.all()
    return render(request, 'manage_patient.html', {"patient":patient})
    


def consult(request):
    cons= Consultant.objects.all()
    return render(request, 'consultant.html', {'cons':cons})




def patient_search(request):
    cons = PatientInfo.objects.all()
    query = request.GET.get('q')
    if query:
        cons = cons.filter(
            Q(id__icontains=query) |
            Q(patientName__icontains=query) |
            Q(doctorName__icontains=query) |
            Q(purpose__icontains=query)
        ).distinct()
    context = {
        'cons': cons,
    }
    return render(request, 'search.html', context)


def home1(request):
    # print(patientName)
    print(loggedinUsers)

    currentPatient = loggedinUsers[-1]

    patientEHRfields = ['Diagnoses', 'Medication', 'Prescription', 'Allergies', 'LabResults', 'ImmunizationDates', 'DoctorNotes', 'BillingInfo']

    for a in patientEHRfields:
        filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/' + a + '.html'
        # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/' + a + '.html'
        # print(filepath)
        encomm = "cpabe-enc pub_key " + filepath + " 'Senior_Doctor or Ortho or Gynaecology or Billing'"
        os.system(encomm)
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        member = Member(username=request.POST['username'], password=request.POST['password'],  firstname=request.POST['firstname'], lastname=request.POST['lastname'])
        member.save()
        return redirect('ehr/')
    else:
        return render(request, 'ehr/register.html')

def login(request):
    return render(request, 'home.html')

def home(request):
    if request.method == 'POST':
        if Member.objects.filter(username=request.POST['username'], password=request.POST['password']).exists():
            member = Member.objects.get(username=request.POST['username'], password=request.POST['password'])
            return render(request, 'web/home.html', {'member': member})
        else:
            context = {'msg': 'Invalid username or password'}
            return render(request, 'ehr/login.html', context)


def stafflogin_view(request):
    uid = request.GET.get('uid', '')
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')

    staffData = StaffInfo.objects.all()

    for sD in staffData:
        if ((sD.uid == uid) and (sD.username == username) and (sD.password == password)):

            #Update global array of logged in Users (Staff)
            loggedinUsers.append(username)
            print(username)
            print(loggedinUsers)
            a = loggedinUsers[0]
            print(a)

            #Get user's attributes
            uAttr = [sD.role, sD.specialization, sD.certification, sD.hward]
            attributes.extend(uAttr)
            #print(attributes)

            # If login creds are correct, then filter patients of the same ward
            patientData = []
            patients = PatientInfo.objects.all()
            # print(patients)

            for p in patients:
                # print (p.patientHward, sD.hward)
                if (p.patientHward == sD.hward):
                    # print ("here")
                    patientData.append(p)

                #Should add searchability here

            # print(patientData.patientName)

            return render(request, 'patientselectTEST.html', {'doctorName' : username, 'patientData' : patientData})

    html = "<html><body> Invalid login credentials provided..! <p> Please go back and try login using your credentials or create a new account by signing up.</p> </body> </html>"
    return HttpResponse(html)

def staffsignup(request):

    return render(request, 'staffsignup.html')

def stafflogin(request):
    return render(request, 'stafflogin.html')

# This function is saving new staff info in the database, need to check if the ontology is populating?
def staffsignup_view(request):
    uid = request.GET.get('uid', '')
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    role = request.GET.get('role', '')
    certification = request.GET.get('certification', '')
    specialization = request.GET.get('specialization', '')
    hward = request.GET.get('hward', '')

    staffData = StaffInfo.objects.all()

    for sD in staffData:
        if sD.uid == uid:
            html = "<html><body> User aready exists..! <p> Your username is %s, please go back and login using your credentials. </p> </body> </html>" %sD.username
            return HttpResponse(html)

    newUser = StaffInfo(uid = uid, username = username, password = password, role = role, certification = certification, specialization = specialization, hward = hward)
    newUser.save()
    return render(request, 'stafflogin.html')

# Should I incorporate ontology here?

class AddPatientView(CreateView):
    form_class = PatientForm
    template_name = 'patientsignup.html'
    success_url = '/home/'

from django.urls import reverse_lazy
class AddPharmacyView(CreateView):
    form_class = PharmacyForm
    template_name = 'pharmacy.html'
    success_url = reverse_lazy('pharmacy')
    success_message = 'New Drug successfully added'



class PharmacyList(ListView):
    template_name = 'pharmacylist.html'

def pharmacylist(request):
    return render(request, 'pharmacylist.html')

def pharmacydetail(request):
    ph = Pharmacy.objects.all()
    return render(request, 'pharmacydetail.html')

class PharmacyDetail(DetailView):
    model = Pharmacy
    template_name = "pharmacydetail.html"


def patientsignup(request):
    form = PatientForm()
    return render(request, 'patientsignup.html', {'form':form})

def patientlogin(request):
    return render(request, 'patientlogin.html')

def patientsignup_view(request):
    patientName = request.GET.get('patientName', '')
    patientPassword = request.GET.get('patientPassword', '')
    secret_key = request.GET.get('secret_key', '')
    purpose = request.GET.get('purpose', '')
    doctorName = request.GET.get('doctorName', '')
    patientHward = request.GET.get('patientHward', '')
    Date_of_Birth = request.GET.get('Date_of_Birth', '')
    Gender = request.GET.get('Gender', '')
    Marital_status = request.GET.get('Marital_status', '')
    Blood_Group = request.GET.get('Blood_Group', '')
    Genotype = request.GET.get('Genotype', '')
    Phone_no = request.GET.get('Phone_no', '')
    Illness = request.GET.get('Illness', '')
    Medical_history = request.GET.get('Medical_history', '')
    Resident_Address = request.GET.get('Resident_Address', '')
    Allegies = request.GET.get('Allegies', '')


    patientData = PatientInfo.objects.all()

    for pD in patientData:
        if pD.patientName   == patientName:
            html = "<html><body> User aready exists..! <p> Your username is %s, please go back and login using your credentials. </p> </body> </html>" %pD.patientName
            return HttpResponse(html)

    newUser = PatientInfo(patientName = patientName, patientPassword = patientPassword, secret_key = secret_key, patientHward = patientHward, purpose= purpose, doctorName=doctorName, Date_of_Birth=Date_of_Birth,
    Gender=Gender,Marital_status=Marital_status,Blood_Group=Blood_Group,Genotype=Genotype,Phone_no=Phone_no,Illness=Illness,Medical_history=Medical_history,Resident_Address=Resident_Address,Allegies=Allegies )
    newUser.save()
    return render(request, 'patientlogin.html')


def patientlogin_view(request):
    patientName = request.GET.get('patientName', '')
    patientPassword = request.GET.get('patientPassword', '')

    print(patientName)

    patientData = PatientInfo.objects.all()

    for pD in patientData:
        if ((pD.patientName == patientName) and (pD.patientPassword == patientPassword)):
            print('Patient ID ::', pD.id)
            loggedinUsers.extend(['None', patientName])
            patientEHRfields = ['Diagnoses', 'Medication', 'Prescription', 'Allergies', 'LabResults', 'ImmunizationDates', 'DoctorNotes', 'BillingInfo']
            return render(request, "patientehrview.html", {'allowedFields':patientEHRfields, 'patientName' : patientName})

    return render(request, "patientlogin.html", {'error_flag' : True})

def runSPARQL(doctorName, patientName):
    g = Graph()
    g.parse("/home/nasim/Desktop/EHR/EHROntology_v2.owl")

    sparql = "SELECT ?predicate WHERE {<http://www.semanticweb.org/umbcknacc/ontologies/2017/10/untitled-ontology-3#" + str(doctorName) + "> ?predicate ?object .}"

    qres = g.query(sparql)

    res = []
    for row in qres:
        # print(row[0])
        # print(type(row))
        p = row[0].split('#')[1]
        # print(p)
        if (p.startswith('can')):
            permission = str(p[3])
            if (permission == 'M'):
                field = str(p[9:])
            else:
                field = str(p[7:])

            if (field and permission):
                if field != 'VitalStats':
                    res.append((field, permission))

    return res

def search(request):
    query = request.GET.get('query', '')

    start_time = time.perf_counter()

    pairing_group = PairingGroup('MNT224')

    cpabe = MMLWL16(pairing_group, 2)

    patientData = []
    patients = PatientInfo.objects.all()

    with open('PK.data', 'rb') as filehandle:
        BytePK = pickle.load(filehandle)
        filehandle.close()

    pk = byToOb(BytePK)

    with open('Key.data', 'rb') as filehandle:
        ByteKey = pickle.load(filehandle)
        filehandle.close()

    key = byToOb(ByteKey)

    token1 = cpabe.Token(pk, query, key)

    print(time.perf_counter() - start_time, "seconds")

    with open('EHRindexThreePatient.data', 'rb') as filehandle:
        ByteCTXT = pickle.load(filehandle)
        filehandle.close()

    Indexes = byToOb(ByteCTXT)
    # b = ctxt[0]
    # c = {'policy': (ORTHO and GYNAECOLOGY)}
    # c.update(b)

    # ctxt[0] = c

    # Indexes = []
    # Indexes.append(ctxt[0])
    # Indexes.append(ctxt[1])

    # policy_str = '((Ortho) and (Gynaecology))'


    for p in patients:
        for ind in Indexes:
            print(ind)
            for i in range(1):
                c = cpabe.policy()
                c.update(ind[i])
                b1 = cpabe.decrypt(pk, c, token1)
                # print(ind[i])
                for x in range(1,2):
                    if b1 == True and p.patientName == ind[x] and p not in patientData:
                        print(p)
                        patientData.append(p)

    return render(request, 'patientselectTESTcopy.html', {'doctorName' : loggedinUsers[-1], 'patientData' : patientData})


def getSelectedPatient(request):
    selectedPatient = request.GET.get('checks')
    loggedinUsers.append(selectedPatient)
    print(loggedinUsers)
    # currentDoctor = loggedinUsers[0]
    currentDoctor = loggedinUsers[-2]

    print(selectedPatient)
    print(currentDoctor)
    print(loggedinUsers)

    fieldsWithPermissions = []
    allowedFiles = []

    fieldsWithPermissions.extend(runSPARQL(currentDoctor, selectedPatient))
    #print (fieldsWithPermissions)

    if (fieldsWithPermissions == []):
        # Need to put a home button here
        return HttpResponse("Access Denied!")

    else:
        # allowedFiles = []
        # print(allowedFiles)
        allowedFiles.extend(fieldsWithPermissions)
        print (allowedFiles)
        for f in allowedFiles:
            # print(f[0])
            # x = f[0]
            # print(x)
            # Allowed_Fields.extend(f)
            if f[0] not in Allowed_Fields:
                Allowed_Fields.append(f[0])
        print(Allowed_Fields)
        return render(request, "patientehrdetails.html", {'allowedFields':allowedFiles, 'patientName' : selectedPatient, 'doctorName' : currentDoctor, 'role' : attributes[0], 'specialization' : attributes[1], 'certification' : attributes[2], 'hward' : attributes[3]})

@xframe_options_sameorigin
def LabResults(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/LabResults.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/LabResults.html'
    cpabefile = filepath + '.cpabe'


    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()
    #print(filecontents)
    #print(type(filecontents))


    # if os.path.isfile(filepath):
    #	print('Ready to Encrypt')
        # encom = "cpabe-enc pub_key" + filepath + " 'Senior_Doctor or Ortho'"
        # os.system(encom)

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def Prescription(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/Prescription.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/Prescription.html'
    cpabefile = filepath + '.cpabe'

    if os.path.isfile(cpabefile):
        print("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
    # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def Medication(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/Medication.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/Medication.html'
    cpabefile = filepath + '.cpabe'

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()
    #print(filecontents)

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def Allergies(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    #print(currentPatient)
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/Allergies.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/Allergies.html'
    cpabefile = filepath + '.cpabe'
    #print(cpabefile)

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()
    #print(filecontents)
    #print(type(filecontents))

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def DoctorNotes(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/DoctorNotes.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/DoctorNotes.html'
    cpabefile = filepath + '.cpabe'

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)

    f = open(filepath, 'r')
    filecontents = f.read()

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def Diagnoses(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    #print(loggedinUsers[1])
    #print(currentPatient)
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/Diagnoses.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/Diagnoses.html'
    #print(filepath)
    cpabefile = filepath + '.cpabe'
    #print(cpabefile)

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    #print(f)
    filecontents = f.read()
    #print(filecontents)

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def ImmunizationDates(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/ImmunizationDates.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/ImmunizationDates.html'
    cpabefile = filepath + '.cpabe'

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()

    return HttpResponse(filecontents)

@xframe_options_sameorigin
def BillingInfo(request):
    # currentPatient = loggedinUsers[1]
    currentPatient = loggedinUsers[-1]
    print(currentPatient)
    filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/BillingInfo.html'
    # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/BillingInfo.html'
    cpabefile = filepath + '.cpabe'

    if os.path.isfile(cpabefile):
        print ("FOUND")
        decomm = "cpabe-dec pub_key priv_key " + filepath + '.cpabe'
        os.system(decomm)
        # print ("Exception raised")

    f = open(filepath, 'r')
    filecontents = f.read()

    return HttpResponse(filecontents)

@csrf_exempt
@xframe_options_sameorigin
def saveEdits(request):
    print(loggedinUsers)
    currentPatient = loggedinUsers[-1]
    # currentDoctor = loggedinUsers[0]
    currentDoctor = loggedinUsers[-2]

    print(currentPatient)
    print(currentDoctor)

    print(Allowed_Fields)

    editField = request.GET.get('select')
    print(editField)
    print (str(editField))

    newEdits = request.GET.get('inputEdit')
    print(newEdits)
    print (str(newEdits))

    if (not editField):
        # print(fieldsWithPermissions)
        # print(allowedFiles)
        # print(AllowedFields)
        # print(type(allowedFiles))
        for EHR_Field in Allowed_Fields:
        # for a in allowedFiles:
            # print(a)
            # b = 0
            # print(a[b])
            # EHR_Field = a[b]
            filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/' + EHR_Field + '.html'
            # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/' + EHR_Field + '.html'
            # print(filepath)
            encomm = "cpabe-enc pub_key " + filepath + " 'Senior_Doctor or Ortho or Gynaecology or Billing'"
            os.system(encomm)

        return render(request, "home.html")
        # return redirect('home.html')

    print (allowedFiles)
    editFieldIndex = [a[0] for a in allowedFiles].index(editField)
    print (editFieldIndex)
    print (fieldsWithPermissions)
    fieldpermission = fieldsWithPermissions[editFieldIndex][1]
    print (fieldpermission)

    if fieldpermission != 'M':
        html = "<html><body> You do not have edit access"
        return HttpResponse(html)

    else:
        # os.system("cpabe-keygen -o priv_key pub_key master_key Ortho Gynaecology Billing Senior_Doctor")
        filepath = '/home/nasim/Desktop/EHR/PatientEHRs/' + currentPatient + '/' + editField + '.html'
        # filepath = '/afs/umbc.edu/users/r/w/rwalid1/home/EHR_application/django_test_r/PatientEHRs/' + currentPatient + '/' + editField + '.html'
        f = open(filepath, 'a+')
        f.write("<p>")
        f.write(newEdits)
        f.write("</p>")

        conts = f.read()
        print (conts)
        encomm = "cpabe-enc pub_key " + filepath + " 'Senior_Doctor or Ortho or Gynaecology or Billing'"
        os.system(encomm)
        return render(request, "patientehrdetails.html", {'allowedFields':allowedFiles, 'patientName' : currentPatient, 'doctorName' : currentDoctor, 'role' : attributes[0], 'specialization' : attributes[1], 'certification' : attributes[2], 'hward' : attributes[3]})

