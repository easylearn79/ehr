from django import forms
from django.forms import DateInput, TextInput

from .models import *
from .models import Pharmacy, Laboratory,PatientInfo, Pharmacy,Laboratory

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class LabForm(FormSettings):
    class Meta:
        model = Laboratory
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class PatientForm(FormSettings):

    class Meta:
        model = PatientInfo
        fields = ['patientName', 'patientPassword', 'secret_key','purpose','doctorName','patientHward','Date_of_Birth','Gender',
        'Marital_status','Blood_Group','Genotype','Phone_no','Illness','Medical_history','Resident_Address','Allegies' ]
        widgets = {
            'Date_of_Birth': DateInput()
        }

class PharmacyForm(FormSettings):
    class Meta:
        model = Pharmacy
        fields = ['Drug_name','Cost','Category','Selling_price', 'Qty','Man_date','Exp_date']
        widgets = {
            'Man_date': DateInput(),
            'Exp_date':DateInput()
        }
        
      

