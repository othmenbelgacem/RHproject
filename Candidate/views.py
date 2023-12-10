from .models import Candidate
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CandidateForm
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np

def index(request):
    candidates = Candidate.objects.all()
#000
    data = {
        'salary': [candidate.salary for candidate in candidates],
        'experience': [candidate.Years_of_Experience for candidate in candidates],
        'gpa': [candidate.gpa for candidate in candidates],
    }
    df = pd.DataFrame(data)

    # Perform linear regression
    X_regression = df[['experience']]  # Swap 'salary' with 'experience'
    y_regression = df['salary']
    model_regression = LinearRegression()
    model_regression.fit(X_regression, y_regression)
    df['salary_pred'] = model_regression.predict(X_regression)

    # Plot the linear regression line with inverted axes
    plt.figure(figsize=(8, 5))
    plt.scatter(df['experience'], df['salary'], label='Actual Data')  # Swap 'salary' with 'experience'
    plt.plot(df['experience'], df['salary_pred'], color='red',
             label='Linear Regression')  # Swap 'salary' with 'experience'
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')  # Swap 'salary' with 'experience'
    plt.legend()

    # Save the linear regression plot to a BytesIO object
    linear_regression_stream = BytesIO()
    plt.savefig(linear_regression_stream, format='png')
    plt.close()

    # Convert the linear regression image stream to base64 for embedding in HTML
    linear_regression_plot_base64 = base64.b64encode(linear_regression_stream.getvalue()).decode('utf-8')

    X_clustering = df[['gpa', 'experience']]
    linkage_matrix = linkage(X_clustering, method='ward')

    # Plot the dendrogram
    plt.figure(figsize=(8, 5))
    dendrogram(linkage_matrix, labels=df.index, orientation='top', distance_sort='descending', show_leaf_counts=True)
    plt.title('Ascending Hierarchical Classification')
    plt.xlabel('Candidates')
    plt.ylabel('Dissimilarity')  # Change 'Age' to an appropriate label
    plt.tight_layout()

    # Save the hierarchical clustering dendrogram plot to a BytesIO object
    dendrogram_stream = BytesIO()
    plt.savefig(dendrogram_stream, format='png')
    plt.close()

    # Convert the dendrogram image stream to base64 for embedding in HTML
    dendrogram_plot_base64 = base64.b64encode(dendrogram_stream.getvalue()).decode('utf-8')

    return render(request, 'Candidate/index.html', {
        'Candidate': candidates,
        'linear_regression_plot': linear_regression_plot_base64,
        'dendrogram_plot': dendrogram_plot_base64,
    })

def view_candidate(request, id):
    candidate = Candidate.objects.get(pk=id)
    return render(request, 'Candidate/view_candidate.html', {'candidate': candidate})


def add(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            #new_cadidature_number = form.cleaned_data['Candidate_number']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_Job_Category = form.cleaned_data['Candidate_job_category']
            new_gpa = form.cleaned_data['gpa']
            new_Years_of_Experience = form.cleaned_data['Years_of_Experience']
            new_salary =form.cleaned_data['salary']
            new_skills =form.cleaned_data['skills']

            new_Candidate = Candidate(
                #Candidate_number=new_cadidature_number,
                first_name=new_first_name,
                last_name=new_last_name,
                email=new_email,
                Candidate_job_category=new_Job_Category,
                gpa=new_gpa,
                Years_of_Experience=new_Years_of_Experience,
                salary = new_salary,
                skills =new_skills
            )

            new_Candidate.save()

            return render(request, 'Candidate/add.html', {
                'form': CandidateForm(),
                'success': True
            })
    else:
        form = CandidateForm()
        return render(request, 'Candidate/add.html', {'form': form})


def edit(request, id):
    if request.method == 'POST':
        candidate = Candidate.objects.get(pk=id)
        form = CandidateForm(request.POST, instance=candidate)  # Use the specific instance
        if form.is_valid():
            form.save()
            return render(request, 'Candidate/edit.html', {
                'form': form,
                'success': True
            })
    else:
        candidate = Candidate.objects.get(pk=id)
        form = CandidateForm(instance=candidate)

    return render(request, 'Candidate/edit.html', {
        'form': form
    })


def delete(request, id):
    if request.method == 'POST':
        candidate = Candidate.objects.get(pk=id)
        candidate.delete()
    return HttpResponseRedirect(reverse('index'))


from django.test import TestCase

# Create your tests here.