from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization
from studentorg.forms import OrganizationForm

from studentorg.models import OrgMember
from studentorg.models import College
from studentorg.models import Program

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = 'home.html'

# Organization
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                            Q(description__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# Org. Members
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrganizationForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrganizationForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

# Student
class StudentList(ListView):
    model = OrgMember
    context_object_name = 'student'
    template_name = 'student_list.html'

class StudentCreateView(CreateView):
    model = OrgMember
    form_class = OrganizationForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = OrgMember
    form_class = OrganizationForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = OrgMember
    template_name ='student_del.html'
    success_url = reverse_lazy('student-list')

# College
class CollegeList(ListView):
    model = College
    context_object_name ='college'
    template_name ='college_list.html'

class CollegeCreateView(CreateView):
    model = College
    form_class = OrganizationForm
    template_name ='college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = OrganizationForm
    template_name ='college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name ='college_del.html'
    success_url = reverse_lazy('college-list')

# Program
class ProgramList(ListView):
    model = Program
    context_object_name ='program'
    template_name ='program_list.html'

class ProgramCreateView(CreateView):
    model = Program
    form_class = OrganizationForm
    template_name ='program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = OrganizationForm
    template_name ='program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name ='program_del.html'
    success_url = reverse_lazy('program-list')


# Create your views here.
