from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from studentorg.models import Organization, Student, OrgMember, College, Program
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm

# Dashboard
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_organizations'] = Organization.objects.count()
        context['total_students'] = Student.objects.count()
        context['total_members'] = OrgMember.objects.count()
        context['total_programs'] = Program.objects.count()
        return context

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = 'dashboard.html'

# Organization Views
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

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

# Org Member Views
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(student__lastname__icontains=query) |
                Q(student__firstname__icontains=query) |
                Q(organization__name__icontains=query)
            )
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

# Student Views
class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(firstname__icontains=query) |
                Q(lastname__icontains=query)
            )
        return queryset

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

# College Views
class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

# Program Views
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(prog_name__icontains=query)
        return queryset

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')

# Chart Data Views
def timeline_chart(request):
    data = OrgMember.objects.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')
    
    return JsonResponse({
        'labels': [item['date'].strftime('%Y-%m-%d') for item in data],
        'datasets': [{
            'label': 'New Members',
            'data': [item['count'] for item in data],
            'fill': False,
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.1
        }]
    })

def popular_organizations_chart(request):
    data = Organization.objects.annotate(
        member_count=Count('orgmember')
    ).values('name', 'member_count').order_by('-member_count')[:5]
    
    return JsonResponse({
        'labels': [item['name'] for item in data],
        'datasets': [{
            'label': 'Number of Members',
            'data': [item['member_count'] for item in data],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ]
        }]
    })

def membership_distribution(request):
    data = College.objects.annotate(
        member_count=Count('program__student__orgmember')
    ).values('college_name', 'member_count')
    
    return JsonResponse({
        'labels': [item['college_name'] for item in data],
        'datasets': [{
            'data': [item['member_count'] for item in data],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)'
            ]
        }]
    })

def bubble_chart_data(request):
    colleges = College.objects.all()
    datasets = []
    
    for college in colleges:
        member_count = OrgMember.objects.filter(student__program__college=college).count()
        org_count = Organization.objects.filter(orgmember__student__program__college=college).distinct().count()
        student_count = Student.objects.filter(program__college=college).count()
        
        datasets.append({
            'label': college.college_name,
            'data': [{
                'x': member_count,
                'y': org_count,
                'r': student_count / 10  # Adjust bubble size
            }]
        })
    
    return JsonResponse({'datasets': datasets})

def scatter_plot_data(request):
    colleges = College.objects.all()
    datasets = []
    
    for college in colleges:
        org_count = Organization.objects.filter(orgmember__student__program__college=college).distinct().count()
        member_count = OrgMember.objects.filter(student__program__college=college).count()
        
        datasets.append({
            'label': college.college_name,
            'data': [{
                'x': org_count,
                'y': member_count,
                'college': college.college_name
            }]
        })
    
    return JsonResponse({'datasets': datasets})
