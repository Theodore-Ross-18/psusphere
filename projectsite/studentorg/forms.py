from django.forms import ModelForm
from django import forms
from .models import Organization
# new added models
from .models import OrgMember
from .models import Student 
from .models import College
from .models import Program

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

class OrgMemberForm(forms.ModelForm):
    class Meta:
        model = OrgMember
        fields = ['student', 'organization']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'lastname', 'firstname', 'program']


class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        fields = ['college_name']


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['prog_name', 'college']