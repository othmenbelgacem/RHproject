from django import forms
from .models import Candidate

class CandidateForm(forms.ModelForm):
    class Meta :
        model = Candidate
        fields=['Candidate_number','first_name','last_name','email','Candidate_job_category','gpa','Years_of_Experience','salary','skills']
        labels ={
            'Candidate_number' :'Candidate Number',
            'first_name':'First Name ',
            'last_name':'Last Name',
            'email': 'Email',
            'Candidate_job_category':'Job Category',
            'gpa':'Age',
            'Years_of_Experience':'Years of Experience',
            'salary':'Salary',
            'skills':'Skills',

        }
        widgets = {
            'Candidate_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'Candidate_job_category': forms.TextInput(attrs={'class': 'form-control'}),
            'gpa': forms.NumberInput(attrs={'class': 'form-control'}),
            'Years_of_Experience':forms.NumberInput(attrs={'class': 'form-control'}),
            'salary':forms.NumberInput(attrs={'class': 'form-control'}),
            'skills':forms.TextInput(attrs={'class': 'form-control'}),
        }





from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.view_candidate, name='view_candidate'),
    path('add/', views.add, name='add'),
path('edit/<int:id>/', views.edit, name='edit'),
path('delete/<int:id>/', views.delete, name='delete'),
]

