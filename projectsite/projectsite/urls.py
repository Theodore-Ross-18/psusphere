"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import (HomePageView, 
                            OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView,
                            OrgMemberList, OrgMemberCreateView, OrgMemberUpdateView, OrgMemberDeleteView,
                            StudentList, StudentCreateView, StudentUpdateView, StudentDeleteView,
                            CollegeList, CollegeCreateView, CollegeUpdateView, CollegeDeleteView,
                            ProgramList, ProgramCreateView, ProgramUpdateView, ProgramDeleteView)  # Added Program views

from studentorg import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    # Organization List
    path('organization_list/', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add/', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<int:pk>/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<int:pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),
    
    # Org. Members
    path('orgmember/', OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember/add/', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember/<int:pk>/', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember/<int:pk>/delete/', OrgMemberDeleteView.as_view(), name='orgmember-delete'),

    # Student
        path('student/', StudentList.as_view(), name='student-list'),
        path('student/add/', StudentCreateView.as_view(), name='student-add'),
        path('student/<int:pk>/', StudentUpdateView.as_view(), name='student-update'),
        path('student/<int:pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    # Login/Logout 
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    
    # College URLs
    path('college/', CollegeList.as_view(), name='college-list'),
    path('college/add/', CollegeCreateView.as_view(), name='college-add'),
    path('college/<int:pk>/', CollegeUpdateView.as_view(), name='college-update'),
    path('college/<int:pk>/delete/', CollegeDeleteView.as_view(), name='college-delete'),
    
    # Program URLs
    path('program/', ProgramList.as_view(), name='program-list'),
    path('program/add/', ProgramCreateView.as_view(), name='program-add'),
    path('program/<int:pk>/', ProgramUpdateView.as_view(), name='program-update'),
    path('program/<int:pk>/delete/', ProgramDeleteView.as_view(), name='program-delete'),
]
